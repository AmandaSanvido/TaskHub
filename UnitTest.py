import unittest
import sqlite3
from datetime import datetime
from unittest.mock import patch
from io import StringIO
from your_module_name import create_database, add_task, assign_task, list_tasks

class TestTaskHubFunctions(unittest.TestCase):

    def setUp(self):
        # Executa antes de cada teste
        create_database()

    def tearDown(self):
        # Executa após cada teste
        connection = sqlite3.connect('taskhub.db')
        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS tasks')
        connection.commit()
        connection.close()

    @patch('builtins.input', side_effect=['20-12-2023'])  # Fornece uma data fixa para o teste
    def test_add_task(self, mock_input):
        # Testa a função add_task
        priority_tag = 'Alta'
        title = 'Test Task'
        description = 'Test Description'
        assignee = 'John Doe'

        # Captura a saída padrão
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            add_task(priority_tag, title, description, assignee)

        # Obtém a saída
        output = mock_stdout.getvalue().strip()
        
        # Verifica se a saída contém a mensagem esperada
        self.assertTrue("Task criada!" in output)
        self.assertTrue("ID:" in output)

    def test_assign_task(self):
        # Testa a função assign_task
        priority_tag = 'Alta'
        title = 'Test Task'
        description = 'Test Description'
        assignee = 'John Doe'
        add_task(priority_tag, title, description, assignee)

        # Obtém o ID da última task criada
        connection = sqlite3.connect('taskhub.db')
        cursor = connection.cursor()
        cursor.execute('SELECT MAX(id) FROM tasks')
        task_id = cursor.fetchone()[0]
        connection.close()

        new_assignee = 'Jane Doe'

        # Captura a saída padrão
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            assign_task(task_id, new_assignee)

        # Obtém a saída
        output = mock_stdout.getvalue().strip()

        # Verifica se a saída contém a mensagem esperada
        self.assertEqual(output, "Task atribuída!")

    def test_list_tasks(self):
        # Testa a função list_tasks
        priority_tag = 'Alta'
        title = 'Test Task'
        description = 'Test Description'
        assignee = 'John Doe'
        add_task(priority_tag, title, description, assignee)

        # Captura a saída padrão
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            list_tasks()

        # Obtém a saída
        output = mock_stdout.getvalue().strip()

        # Verifica se a saída contém a informação da task criada
        self.assertTrue("Task ID:" in output)
        self.assertTrue("Prioridade:" in output)
        self.assertTrue("Título:" in output)
        self.assertTrue("Descrição:" in output)
        self.assertTrue("Atribuído à:" in output)
        self.assertTrue("Status:" in output)
        self.assertTrue("Prazo:" in output)

if __name__ == '__main__':
    unittest.main()
