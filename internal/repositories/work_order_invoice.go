package repositories

import (
	"context"
	"database/sql"
	"time"

	"github.com/over55/workery-server/internal/models"
)

type WorkOrderInvoiceRepo struct {
	db *sql.DB
}

func NewWorkOrderInvoiceRepo(db *sql.DB) *WorkOrderInvoiceRepo {
	return &WorkOrderInvoiceRepo{
		db: db,
	}
}

func (r *WorkOrderInvoiceRepo) Insert(ctx context.Context, m *models.WorkOrderInvoice) error {
	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	query := `
    INSERT INTO work_order_invoices (
        uuid, tenant_id, old_id, invoice_id, order_id, invoice_date,
		associate_name, associate_telephone, client_name, client_telephone,
		client_email,
		line_01_qty, line_01_desc, line_01_price, line_01_amount,
		line_02_qty, line_02_desc, line_02_price, line_02_amount,
		line_03_qty, line_03_desc, line_03_price, line_03_amount,
		line_04_qty, line_04_desc, line_04_price, line_04_amount,
		line_05_qty, line_05_desc, line_05_price, line_05_amount,
		line_06_qty, line_06_desc, line_06_price, line_06_amount,
		line_07_qty, line_07_desc, line_07_price, line_07_amount,
		line_08_qty, line_08_desc, line_08_price, line_08_amount,
		line_09_qty, line_09_desc, line_09_price, line_09_amount,
		line_10_qty, line_10_desc, line_10_price, line_10_amount
    ) VALUES (
        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16,
		$17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31,
		$32, $33, $34, $35, $36, $37, $38, $39, $40, $41, $42, $43, $44, $45,
		$46, $47, $48, $49, $50, $51
    )`
	stmt, err := r.db.PrepareContext(ctx, query)
	if err != nil {
		return err
	}
	defer stmt.Close()

	_, err = stmt.ExecContext(
		ctx,
		m.Uuid, m.TenantId, m.OldId, m.InvoiceId, m.OrderId, m.InvoiceDate,
		m.AssociateName, m.AssociateTelephone, m.ClientName, m.ClientTelephone,
		m.ClientEmail,
		m.Line01Qty, m.Line01Desc, m.Line01Price, m.Line01Amount,
		m.Line02Qty, m.Line02Desc, m.Line02Price, m.Line02Amount,
		m.Line03Qty, m.Line03Desc, m.Line03Price, m.Line03Amount,
		m.Line04Qty, m.Line04Desc, m.Line04Price, m.Line04Amount,
		m.Line05Qty, m.Line05Desc, m.Line05Price, m.Line05Amount,
		m.Line06Qty, m.Line06Desc, m.Line06Price, m.Line06Amount,
		m.Line07Qty, m.Line07Desc, m.Line07Price, m.Line07Amount,
		m.Line08Qty, m.Line08Desc, m.Line08Price, m.Line08Amount,
		m.Line09Qty, m.Line09Desc, m.Line09Price, m.Line09Amount,
		m.Line10Qty, m.Line10Desc, m.Line10Price, m.Line10Amount,
	)
	return err
}

func (r *WorkOrderInvoiceRepo) UpdateById(ctx context.Context, m *models.WorkOrderInvoice) error {
	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	query := `
    UPDATE
        work_order_invoices
    SET
        tenant_id = $1
    WHERE
        id = $2`
	stmt, err := r.db.PrepareContext(ctx, query)
	if err != nil {
		return err
	}
	defer stmt.Close()

	_, err = stmt.ExecContext(
		ctx,
		m.TenantId, m.Id,
	)
	return err
}

func (r *WorkOrderInvoiceRepo) GetById(ctx context.Context, id uint64) (*models.WorkOrderInvoice, error) {
	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	m := new(models.WorkOrderInvoice)

	query := `
    SELECT
        id, uuid, tenant_id
	FROM
        work_order_invoices
    WHERE
        id = $1`
	err := r.db.QueryRowContext(ctx, query, id).Scan(
		&m.Id, &m.Uuid, &m.TenantId,
	)
	if err != nil {
		// CASE 1 OF 2: Cannot find record with that email.
		if err == sql.ErrNoRows {
			return nil, nil
		} else { // CASE 2 OF 2: All other errors.
			return nil, err
		}
	}
	return m, nil
}

func (r *WorkOrderInvoiceRepo) GetByOld(ctx context.Context, tenantId uint64, oldId uint64) (*models.WorkOrderInvoice, error) {
	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	m := new(models.WorkOrderInvoice)

	query := `
    SELECT
        id, uuid, tenant_id
	FROM
        work_order_invoices
    WHERE
        old_id = $1 AND tenant_id = $2`
	err := r.db.QueryRowContext(ctx, query, oldId, tenantId).Scan(
		&m.Id, &m.Uuid, &m.TenantId,
	)
	if err != nil {
		// CASE 1 OF 2: Cannot find record with that email.
		if err == sql.ErrNoRows {
			return nil, nil
		} else { // CASE 2 OF 2: All other errors.
			return nil, err
		}
	}
	return m, nil
}

func (r *WorkOrderInvoiceRepo) CheckIfExistsById(ctx context.Context, id uint64) (bool, error) {
	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	var exists bool

	query := `
    SELECT
        1
    FROM
        work_order_invoices
    WHERE
        id = $1`
	err := r.db.QueryRowContext(ctx, query, id).Scan(&exists)
	if err != nil {
		// CASE 1 OF 2: Cannot find record with that email.
		if err == sql.ErrNoRows {
			return false, nil
		} else { // CASE 2 OF 2: All other errors.
			return false, err
		}
	}
	return exists, nil
}

func (r *WorkOrderInvoiceRepo) InsertOrUpdateById(ctx context.Context, m *models.WorkOrderInvoice) error {
	if m.Id == 0 {
		return r.Insert(ctx, m)
	}

	doesExist, err := r.CheckIfExistsById(ctx, m.Id)
	if err != nil {
		return err
	}

	if doesExist == false {
		return r.Insert(ctx, m)
	}
	return r.UpdateById(ctx, m)
}
