import os
from datetime import datetime
from typing import Dict, List, Optional

from loguru import logger
from neomodel import config, db

from hashing import get_hash
from models import HashNode


class Repository:
    """
    The Repository class manages the loading, organizing, and checking of files in a hierarchical structure.
    It uses a database connection specified by the provided username and password.

    Attributes:
        roots (dict): Dictionary to store root nodes for each file extension.
    """

    def __init__(self, user: str, password: str, host: str, resources: List[str] = None) -> None:
        """
        Initializes a Repository instance with username, password, and host information.

        Args:
            user (str): Database username.
            password (str): Database password.
            host (str): Database host.
            resources (List[str]): A list of directory paths where files can be found (optional).
        """
        self.user = user
        self.password = password
        self.host = host
        self.resources = resources if resources is not None else []
        self.roots = {}
        config.DATABASE_URL = f'bolt://{user}:{password}@{host}:7687'

    def load_data(self) -> None:
        """
        Loads data from the specified directory and organizes it into a hierarchical structure.
        """
        extensions = self.group_by_extensions()
        print(extensions)
        for key, values in extensions.items():
            try:
                root = HashNode.nodes.get(name=key)
            except HashNode.DoesNotExist:
                root = HashNode(name=key).save()
            self.roots[key] = root
            node_list = []
            logger.info(f"Loading {key}")
            for value in values:
                name = os.path.basename(value)
                new_node = self.find_node_by_name(name)
                if new_node is None:
                    date = datetime.now()
                    new_node = HashNode(name=name, path=value, created_at=date, hash=get_hash(value, date)).save()
                    node_list.append(new_node)
                else:
                    logger.info(f"File {name} already exists")
                    self.check_hash(new_node)
                    new_node.save()
            self.add_node_sorted(root, node_list)

    def group_by_extensions(self) -> Dict[str, List[str]]:
        """
        Groups files by their extensions in the specified directory.

        Returns:
            dict: A dictionary where keys are file extensions and values are lists of file paths.
        """
        extensions = {}
        for resource in self.resources:
            for current_path, subfolders, files in os.walk(resource):
                print(files)
                if not files:
                    continue
                for file in files:
                    extension = os.path.splitext(file)[-1]
                    file_path = os.path.join(current_path, file)
                    if extension in extensions:
                        extensions[extension].append(file_path)
                    else:
                        extensions[extension] = [file_path]
        return extensions

    def find_node(self, root: HashNode, name: str) -> HashNode:
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

    def find_node_by_name(self, name: str) -> HashNode:
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

    def add_node(self, root: HashNode, new_node: HashNode) -> Optional[HashNode]:
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
                logger.info(f"Adding {new_node.name} in LOWER side of {root.name}")
                root.lower.connect(new_node)
            else:
                self.add_node(son, new_node)
        else:
            son = root.upper.single()
            if son is None:
                logger.info(f"Adding {new_node.name} in UPPER side of {root.name}")
                root.upper.connect(new_node)
            else:
                self.add_node(son, new_node)
        return root

    def add_node_by_name(self, name: str) -> None:
        """
        Adds a new node to the hierarchical structure based on the provided file name.

        Args:
            name (str): The name of the file.

        Returns:
            None
        """
        extension = os.path.splitext(name)[-1]
        root = self.roots.get(extension)
        date = datetime.now()
        new_node = HashNode(name=str(os.path.basename(name)), path=str(name), hash=get_hash(name, date),
                            created_at=date).save()
        new_node.save()
        self.add_node(root, new_node)

    def add_node_sorted(self, root: HashNode, node_list: List[HashNode]) -> None:
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

    def get_all(self) -> List[HashNode]:
        """
        Retrieves all nodes from the hierarchical structure.

        Returns:
            QuerySet: All nodes in the hierarchical structure.
        """
        return HashNode.nodes.all()

    def all_files(self) -> None:
        """
        Checks the hash value for all files in the hierarchical structure.
        """
        for node in self.get_all():
            self.check_hash(node)

    def one_file(self, name: str) -> bool:
        """
        Checks the hash value for a specific file in the hierarchical structure.

        Args:
            name (str): The name of the file to check.

        Returns:
            bool: True if the file has been modified, False otherwise.
        """
        node = self.find_node_by_name(name)
        logger.info("Checking file {}".format(name))
        return self.check_hash(node)

    def check_hash(self, node: HashNode) -> bool:
        """
        Checks if the hash value of a node matches the computed hash for the associated file.

        Args:
            node (HashNode): The node to check.

        Returns:
            bool: True if the file has been modified, False otherwise.
        """
        if node.hash != "" and node.hash is not None:
            if node.hash != get_hash(node.path, node.created_at):
                logger.error("File {} has been modified".format(node.path))
                return True
            else:
                logger.info("File {} has not been modified".format(node.path))
                return False

    def delete_all(self):
        """
        Deletes all nodes from the hierarchical structure.
        """
        db.cypher_query("MATCH(n) DETACH DELETE n")
