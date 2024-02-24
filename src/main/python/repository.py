import os

from neomodel import config, db

from src.main.python.hashing import get_hash
from src.main.python.logger import Logger
from src.main.python.models import HashNode


class Repository:

    def __init__(self, user, password):
        """
        Initializes a Repository instance with user and password for database connection.

        Args:
            user (str): Database username.
            password (str): Database password.
        """
        self.user = user
        self.password = password
        self.roots = {}
        self.logger = Logger()
        config.DATABASE_URL = f'bolt://{user}:{password}@localhost:7687'

    def load_data(self):
        """
        Loads data from the specified directory and organizes it into a hierarchical structure.
        """
        extensions = self.group_by_extensions()
        for key, values in extensions.items():
            try:
                root = HashNode.nodes.get(name=key)
            except HashNode.DoesNotExist:
                root = HashNode(name=key)
                root.save()
            self.roots[key] = root
            node_list = []
            self.logger.info(f"Loading {key}")
            for value in values:
                name = os.path.basename(value)
                new_node = self.find_node_by_name(name)
                if new_node is None:
                    new_node = HashNode()
                    new_node.name = str(name)
                    new_node.path = str(value)
                    new_node.hash = get_hash(value)
                    new_node.save()
                    node_list.append(new_node)
                else:
                    self.check_hash(new_node)
                    new_node.save()
            self.add_node_sorted(root, node_list)

    def group_by_extensions(self):
        """
        Groups files by their extensions in the specified directory.

        Returns:
            dict: A dictionary where keys are file extensions and values are lists of file paths.
        """
        extensions = {}
        for current_path, subfolders, files in os.walk("../resources"):
            if current_path == "../resources":
                continue
            for file in files:
                extension = os.path.splitext(file)[-1]
                file_path = os.path.join(current_path, file)
                if extension in extensions:
                    extensions[extension].append(file_path)
                else:
                    extensions[extension] = [file_path]
        return extensions

    def find_node(self, root, name):
        """
        Finds a node with the specified name in the hierarchical structure.

        Args:
            root (HashNode): The root node of the hierarchy.
            name (str): The name of the node to find.

        Returns:
            HashNode or None: The found node or None if not found.
        """
        if root is None:
            return None
        elif root.name == name:
            return root
        elif root.name > name:
            return self.find_node(root.lower.single(), name)
        else:
            return self.find_node(root.upper.single(), name)

    def find_node_by_name(self, name):
        """
        Finds a node with the specified name in the hierarchical structure.

        Args:
            name (str): The name of the node to find.

        Returns:
            HashNode or None: The found node or None if not found.
        """
        extension = os.path.splitext(name)[-1]
        root = self.roots.get(extension)
        return self.find_node(root, name)


    def add_node(self, root, new_node):
        """
        Adds a new node to the hierarchical structure.

        Args:
            root (HashNode): The root node of the hierarchy.
            new_node (HashNode): The node to be added.

        Returns:
            HashNode: The updated root node after adding the new node.
        """
        if root is None:
            return new_node
        elif root.name > new_node.name:
            son = root.lower.single()
            if son is None:
                self.logger.info(f"Adding {new_node.name}")
                root.lower.connect(new_node)
            else:
                self.add_node(son, new_node)
        else:
            son = root.upper.single()
            if son is None:
                self.logger.info(f"Adding {new_node.name}")
                root.upper.connect(new_node)
            else:
                self.add_node(son, new_node)
        return root

    def add_node_by_name(self, name):
        """
        Adds a new node to the hierarchical structure based on the provided file name.

        Args:
            name (str): The name of the file.

        Returns:
            None
        """
        extension = os.path.splitext(name)[-1]
        root = self.roots.get(extension)
        new_node = HashNode()
        new_node.name = str(os.path.basename(name))
        new_node.path = str(name)
        new_node.hash = get_hash(name)
        new_node.save()
        self.add_node(root, new_node)

    def add_node_sorted(self, root, node_list):
        """
        Adds a list of nodes to the hierarchical structure in a sorted order.

        Args:
            root (HashNode): The root node of the hierarchy.
            node_list (list): List of nodes to be added.

        Returns:
            None
        """
        if not node_list:
            return

        mid = len(node_list) // 2
        left_nodes = node_list[:mid]
        right_nodes = node_list[mid + 1:]

        self.add_node(root, node_list[mid])

        self.add_node_sorted(root, left_nodes)
        self.add_node_sorted(root, right_nodes)

    def get_all(self):
        return HashNode.nodes.all()

    def all_files(self):
        for node in self.get_all():
            self.check_hash(node)

    def one_file(self, name):
        node = self.find_node_by_name(name)
        print(name)
        self.check_hash(node)

    def check_hash(self, node):
        if node.hash != "" and node.hash != None:
            if node.hash != get_hash(node.path):
                self.logger.error("File {} has been modified".format(node.path))
            else:
                self.logger.info("File {} has not been modified".format(node.path))


if __name__ == "__main__":
    repository = Repository("neo4j", "12345678")
    # db.cypher_query("MATCH (n) DETACH DELETE n")
    repository.load_data()
    a = repository.find_node_by_name("a.txt")
    print(a)