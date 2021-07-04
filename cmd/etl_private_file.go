package cmd

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"os"
	// "strings"
	"time"

	"github.com/google/uuid"
	"github.com/spf13/cobra"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"

	"github.com/over55/workery-server/internal/models"
	"github.com/over55/workery-server/internal/repositories"
	"github.com/over55/workery-server/internal/utils"
)

var (
	privateFileETLSchemaName string
)

func init() {
	privateFileETLCmd.Flags().StringVarP(&privateFileETLSchemaName, "schema_name", "s", "", "The schema name in the postgres.")
	privateFileETLCmd.MarkFlagRequired("schema_name")
	rootCmd.AddCommand(privateFileETLCmd)
}

var privateFileETLCmd = &cobra.Command{
	Use:   "etl_private_file",
	Short: "Import the private files from the old workery",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		doRunImportPrivateFile()
	},
}

// Special thanks via https://docs.digitalocean.com/products/spaces/resources/s3-sdk-examples/
func getOldS3ClientInstance() (*s3.S3, string) {
	key := os.Getenv("WORKERY_OLD_AWS_S3_ACCESS_KEY")
	secret := os.Getenv("WORKERY_OLD_AWS_S3_SECRET_KEY")
	endpoint := os.Getenv("WORKERY_OLD_AWS_S3_ENDPOINT")
	region := os.Getenv("WORKERY_OLD_AWS_S3_REGION")
	bucketName := os.Getenv("WORKERY_OLD_AWS_S3_BUCKET_NAME")

	s3Config := &aws.Config{
		Credentials: credentials.NewStaticCredentials(key, secret, ""),
		Endpoint:    aws.String(endpoint),
		Region:      aws.String(region),
	}

	newSession := session.New(s3Config)
	s3Client := s3.New(newSession)
	return s3Client, bucketName
}

func listAllS3Objects(s3Client *s3.S3, bucketName string) *s3.ListObjectsOutput {
	input := &s3.ListObjectsInput{
		Bucket: aws.String(bucketName),
	}

	objects, err := s3Client.ListObjects(input)
	if err != nil {
		log.Println(err.Error())
	}

	return objects
}

func doRunImportPrivateFile() {
	// Load up our NEW database.
	db, err := utils.ConnectDB(databaseHost, databasePort, databaseUser, databasePassword, databaseName, "public")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Load up our OLD database.
	oldDBHost := os.Getenv("WORKERY_OLD_DB_HOST")
	oldDBPort := os.Getenv("WORKERY_OLD_DB_PORT")
	oldDBUser := os.Getenv("WORKERY_OLD_DB_USER")
	oldDBPassword := os.Getenv("WORKERY_OLD_DB_PASSWORD")
	oldDBName := os.Getenv("WORKERY_OLD_DB_NAME")
	oldDb, err := utils.ConnectDB(oldDBHost, oldDBPort, oldDBUser, oldDBPassword, oldDBName, privateFileETLSchemaName)
	if err != nil {
		log.Fatal(err)
	}
	defer oldDb.Close()

	// Load up our background context.
	ctx := context.Background()

	// Load up our repositories.
	tr := repositories.NewTenantRepo(db)
	puir := repositories.NewPrivateFileRepo(db)

	// Load up our S3 instances
	oldS3Client, oldBucketName := getOldS3ClientInstance()

	// Lookup the tenant.
	tenant, err := tr.GetBySchemaName(ctx, privateFileETLSchemaName)
	if err != nil {
		log.Fatal(err)
	}
	if tenant == nil {
		log.Fatal("Tenant does not exist!")
	}

	runPrivateFileETL(ctx, tenant.Id, puir, oldDb, oldS3Client, oldBucketName)
}

type OldPrivateFile struct {
	Id                       uint64         `json:"id"`
	DataFile                 string         `json:"data_file"`
	Title                    string         `json:"title"`
	Description                 string         `json:"description"`
	IsArchived               bool           `json:"is_archived"`
	IndexedText              sql.NullString         `json:"indexed_text"`
	CreatedAt                time.Time      `json:"created_at"`
	CreatedFrom              sql.NullString `json:"created_from"`
	CreatedFromIsPublic      bool           `json:"created_from_is_public"`
	CreatedById              sql.NullInt64  `json:"created_by_id"`
	LastModifiedAt           time.Time      `json:"last_modified_at"`
	LastModifiedFrom         sql.NullString `json:"last_modified_from"`
	LastModifiedFromIsPublic bool           `json:"last_modified_from_is_public"`
	LastModifiedById         sql.NullInt64  `json:"last_modified_by_id"`
	AssociateId              sql.NullInt64  `json:"associate_id"`
	CustomerId               sql.NullInt64  `json:"customer_id"`
	PartnerId                sql.NullInt64  `json:"partner_id"`
	StaffId                  sql.NullInt64  `json:"staff_id"`
	WorkOrderId              sql.NullInt64  `json:"work_order_id"`
}

func ListAllPrivateFiles(db *sql.DB) ([]*OldPrivateFile, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	query := `
	SELECT
	    id, data_file, title, description, is_archived, indexed_text, created_at,
		created_from, created_from_is_public, created_by_id, last_modified_at,
		last_modified_from, last_modified_from_is_public, last_modified_by_id,
		associate_id, customer_id, partner_id, staff_id, work_order_id
	FROM
	    workery_private_file_uploads
	ORDER BY
	    id
	ASC
	`
	rows, err := db.QueryContext(ctx, query)
	if err != nil {
		return nil, err
	}

	var arr []*OldPrivateFile
	defer rows.Close()
	for rows.Next() {
		m := new(OldPrivateFile)
		err = rows.Scan(
			&m.Id,
			&m.DataFile,
			&m.Title,
			&m.Description,
			&m.IsArchived,
			&m.IndexedText,
			&m.CreatedAt,
			&m.CreatedFrom,
			&m.CreatedFromIsPublic,
			&m.CreatedById,
			&m.LastModifiedAt,
			&m.LastModifiedFrom,
			&m.LastModifiedFromIsPublic,
			&m.LastModifiedById,
			&m.AssociateId,
			&m.CustomerId,
			&m.PartnerId,
			&m.StaffId,
			&m.WorkOrderId,
		)
		if err != nil {
			panic(err)
		}
		arr = append(arr, m)
	}
	err = rows.Err()
	if err != nil {
		panic(err)
	}
	return arr, err
}

func runPrivateFileETL(
	ctx context.Context,
	tenantId uint64,
	puir *repositories.PrivateFileRepo,
	oldDb *sql.DB,
	oldS3Client *s3.S3,
	oldBucketName string,
) {
	// Fetch all the database records from the old database at once.
	uploads, err := ListAllPrivateFiles(oldDb)
	if err != nil {
		log.Fatal(err)
	}

	// Fetch all the upload files we have in the old AWS S3 instance.
	s3Objects := listAllS3Objects(oldS3Client, oldBucketName)

	// Iterate through all the old database records and iterate over the
	// upload AWS S3 files to match the key, then process the file.
	for _, upload := range uploads {

		key := utils.FindMatchingObjectKeyInS3Bucket(s3Objects, upload.DataFile)

		// for _, obj := range objects.Contents {
		// 	objKey := aws.StringValue(obj.Key)
		//
		// 	match := strings.Contains(objKey, opiu.ImageFile)
		//
		// 	log.Println(objKey, opiu.ImageFile, " | ", match)
		// 	if match == true {
		// 		log.Fatal("PROGRAMMER HALT") //TODO: CONTINUE PROGRAMMING HERE
		// 	}
		// }
		// return
        log.Println(key, "\n\n", upload.DataFile, "\n\n\n\n")

		// insertPrivateFileETL(ctx, tenantId, puir, opiu, oldS3Client, oldBucketName)
	}
}

func insertPrivateFileETL(
	ctx context.Context,
	tid uint64,
	puir *repositories.PrivateFileRepo,
	opiu *OldPrivateFile,
	oldS3Client *s3.S3,
	oldBucketName string,
) {
	//
	input := &s3.GetObjectInput{
		Bucket: aws.String(oldBucketName),
		Key:    aws.String(opiu.DataFile),
	}

	result, err := oldS3Client.GetObject(input)
	if err != nil {
		fmt.Println(err.Error())
	}
	fmt.Println(result)
	fmt.Println(result.Body)
	log.Fatal("PROGRAMMER HALT") //TODO: CONTINUE PROGRAMMING HERE

	m := &models.PrivateFile{
		OldId:              opiu.Id,
		TenantId:           tid,
		Uuid:               uuid.NewString(),
		// ImageFile:          opiu.ImageFile,
		// CreatedTime:        opiu.CreatedAt,
		// CreatedFromIP:      opiu.CreatedFrom.String,
		// LastModifiedTime:   opiu.LastModifiedAt,
		// LastModifiedFromIP: opiu.LastModifiedFrom.String,
		// CreatedById:        opiu.CreatedById,
		// LastModifiedById:   opiu.LastModifiedById,
		State:              1,
	}
	err = puir.Insert(ctx, m)
	if err != nil {
		log.Panic(err)
	}
	fmt.Println("Imported ID#", opiu.Id)
}
