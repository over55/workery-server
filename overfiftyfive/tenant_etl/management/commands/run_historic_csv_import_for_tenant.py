# -*- coding: utf-8 -*-
import csv
import os
import sys
import re
import os.path as ospath
import codecs
from decimal import *
from django.db.models import Sum
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import connection # Used for django tenants.
from django.utils.translation import ugettext_lazy as _
from shared_foundation.models import SharedFranchise
from tenant_foundation.models import Staff
from tenant_etl.utils.csv.associates_importer import run_associates_importer_from_csv_file
from tenant_etl.utils.csv.customer_importer import run_customer_importer_from_csv_file, run_customer_and_org_importer_from_csv_file


"""
Run manually in console:
python manage.py run_historic_csv_import_for_tenant "london" "dev"
"""


class Command(BaseCommand):
    help = _('Command will load up historical data with tenant.')

    def add_arguments(self, parser):
        parser.add_argument('schema_name', nargs='+', type=str)
        parser.add_argument('csv_prefix', nargs='+', type=str)

    def handle(self, *args, **options):
        # Get user inputs.
        schema_name = options['schema_name'][0]
        prefix = options['csv_prefix'][0]

        # Connection needs first to be at the public schema, as this is where
        # the database needs to be set before creating a new tenant. If this is
        # not done then django-tenants will raise a "Can't create tenant outside
        # the public schema." error.
        connection.set_schema_to_public() # Switch to Public.

        try:
            franchise = SharedFranchise.objects.get(schema_name=schema_name)
        except SharedFranchise.DoesNotExist:
            raise CommandError(_('Franchise does not exist!'))

        # Begin importing...
        self.begin_processing(franchise, prefix)

        # Used for debugging purposes.
        self.stdout.write(
            self.style.SUCCESS(_('Successfully imported historic tenant.'))
        )

    # def strip_chars(self, f):
    #     remove_re = re.compile(u'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F%s]'
    #                            % u'')
    #     head,tail = ospath.split(f)
    #     fin = codecs.open(f, encoding = 'utf-8')
    #     fout = codecs.open(head + os.path.sep + 'tmp.csv', mode = 'w', encoding = 'utf-8')
    #     i = 1
    #     stripped = 0
    #     for line in fin:
    #         new_line, count = remove_re.subn('', line)
    #         if count > 0:
    #             plur = ((count > 1) and u's') or u''
    #             sys.stderr.write('Line %d, removed %s character%s.\n'
    #                              % (i, count, plur))
    #
    #         fout.write(new_line)
    #         stripped = stripped + count
    #         i = i + 1
    #     sys.stderr.write('Stripped %d characters from %d lines.\n'
    #                      % (stripped, i))
    #     fin.close()
    #     fout.close()
    #     os.rename(f, head + os.path.sep + 'old_' + tail)
    #     os.rename(head + os.path.sep + 'tmp.csv', f)

    def get_directory(self):
        # Get the directory of this command.
        directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Change root location.
        directory = directory.replace("/management", "/static")

        # Return our directory.
        return directory

    def get_filepaths(self, directory):
        """
        This function will generate the file names in a directory
        tree by walking the tree either top-down or bottom-up. For each
        directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
        """
        file_paths = []  # List which will store all of the full filepaths.

        # Walk the tree.
        for root, directories, files in os.walk(directory):
            for filename in files:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)  # Add it to the list.
        return file_paths  # Self-explanatory.

    def begin_processing(self, franchise, prefix):
        # Connection will set it back to our tenant.
        connection.set_schema(franchise.schema_name, True) # Switch to Tenant.

        # FOR DEBUGGING PURPOSES ONLY. UNCOMMENT AT YOUR OWN RISK!
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # from tenant_foundation.models.customer import Customer
        # from tenant_foundation.models.associate import Associate
        # from django.contrib.auth.models import User
        # Customer.objects.delete_all()
        # Associate.objects.delete_all()
        # SharedUser.objects.all().delete()
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # Get all the files in the directory.
        directory = self.get_directory()
        full_file_paths = self.get_filepaths(directory)

        # Sort the URL's alphabetically.
        full_file_paths = sorted(full_file_paths)

        # Iterate through all the file paths and only process files
        # with a "CSV" filename.
        for full_file_path in full_file_paths:
            if full_file_path.endswith(".csv") and prefix in full_file_path:
                # Import this file into the database based on what type of
                # object it is.
                self.begin_processing_csv(full_file_path)

    def begin_processing_csv(self, full_file_path):
        """
        Function will import the CSV file into the database.
        """
        # self.strip_chars(full_file_path)

        with open(full_file_path, newline='', encoding='utf-8') as csvfile:
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            if "employee.csv" in full_file_path:
                self.stdout.write(
                    self.style.SUCCESS(_('Importing "Associates" at %(path)s ...') % {
                        'path': full_file_path
                    })
                )
                run_associates_importer_from_csv_file(csvfile)
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            if "small_job_employers.csv" in full_file_path:
                self.stdout.write(
                    self.style.SUCCESS(_('Importing "Customers" at %(path)s ...') % {
                        'path': full_file_path
                    })
                )
                run_customer_importer_from_csv_file(csvfile)
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            if "employer.csv" in full_file_path:
                self.stdout.write(
                    self.style.SUCCESS(_('Importing "Customers" and "Organizations" at %(path)s ...') % {
                        'path': full_file_path
                    })
                )
                run_customer_and_org_importer_from_csv_file(csvfile)
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
