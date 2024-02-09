"""
Test custom django management commands.
"""
# For mocking the behavior of the database..
from unittest.mock import patch

# One of the possibilities of the errors that we might get when we try and connect to the database before the database is ready..
from psycopg2 import OperationalError as Psycopg2Error

# Helper function provided by django that allows as to call command that we are testing by its name..
from django.core.management import call_command

# Another exception.. 
from django.db.utils import OperationalError

# BaseTestClass SimpleTestCase because we are testing the behavior that our database is not available therefore we dont need migrations and things like that to be applied to the test..
from django.test import SimpleTestCase

# Mocking the behavior of our database < This is the path that we are going to be mocking > and we are going to mock that check method returning an exception..
@patch('core.management.commands.wait_for_db.Command.check')
class commandTests(SimpleTestCase):
    """Test commands."""

    # patched_check object replaces check is passed due to patch mocking decorator.. 
    # This is one possible test case that we call our command and our database is already ready..
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        
        # This just says when we call mocked check method or when it is called inside our command, we just want it to return our true..  
        patched_check.return_value = True

        # This execute the code inside the wait_for_db and also checks the command is setup correclty and can be called.. 
        call_command('wait_for_db')

        # Ensures the mocked object which is the check method is called once with this parameters..
        patched_check.assert_called_once_with(databases=['default'])
 
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        
        # Here we want to raise some exceptions that would be raised if the data base wasnt ready
        # if we are passes an exception then the mocking library knows that it should raise that exception
        # The first two times we raise Psycopg2Error and the next three times we raise OperationalError atlast it returns True
        # This is found by try and error often what happens is theres different stages of postgres starting, the first stages Postgres the application itself hasn't even started
        # It is not ready to accept any connections in this case you got the psycopg error, after that the database is ready to get connections 
        # But it hasn't set up the testing database that we want to use in that case django raises the operational error
        patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        
        call_command('wait_for_db')

        # We are going to check that our mocked check method is called 6 tims 
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])