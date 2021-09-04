import os
import tempfile
from odoo.tests.common import SingleTransactionCase
from odoo import exceptions


class TestImport(SingleTransactionCase):

    def setUp(self):
        super(TestImport, self).setUp()
        self.settings = self.env["res.config.settings"].create(
            {
                "directory": tempfile.gettempdir(),
            }
        )
        # these are the number of records in the test data minus some
        # wrong ones that won't be imported (invalid data types ex. id column
        # containing chars when it should be an integer.
        self.DEVICES = 9
        self.CONTENT = 19

    def test_import(self):
        # try import from local dir that does not exist
        with self.assertRaises(exceptions.ValidationError):
            self.settings.write({"directory": "/does/not/exist/"})

        # try doing the import with the data provided
        self.settings.write(
            {
                "directory": os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), "data"
                ),
            }
        )
        self.env.ref("12-csv.ir_cron_csv_import").method_direct_trigger()

        # we know some things about the demo files we are importing, lets
        # verify them here
        assert self.env["data.device"].search_count([]) == self.DEVICES
        assert self.env["data.content"].search_count([]) == self.CONTENT
        # TODO tests to be written here
        # an ftps location which is not reachable
        # an ftps location with failed auth
        # an fps location with multiple files including csv
