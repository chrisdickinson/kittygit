from unittest import TestCase
from kittygit import operations
from kittygit.exceptions import KittyGitRepoExists
from nappingcat.exceptions import NappingCatException
import time
import os
import random
import mox
import shutil
import sys

class TestOfForkRepository(TestCase):
    def setUp(self):
        self.cleanup_dirs = []

    def tearDown(self):
        if self.cleanup_dirs:
            for dir in self.cleanup_dirs:
                shutil.rmtree(dir)

    def test_bad_from_dir_raises_exception(self):
        fake_directory = '%d/%d/%d' % (random.randint(1,10), random.randint(1,10), random.randint(1,10))
        doesnt_matter = str(random.randint(1,100))
        self.assertRaises(NappingCatException, operations.fork_repository, doesnt_matter, fake_directory, doesnt_matter)

    def test_existing_target_directory_raises_exception(self):
        doesnt_matter = random.randint(1,100)
        directory = ".test-%d"
        os.makedirs(directory)
        self.assertRaises(KittyGitRepoExists, operations.fork_repository, doesnt_matter, directory, directory) 
        shutil.rmtree(directory)

    def test_actually_forks_repository(self):
        from_dir, to_dir = ".%d" % random.randint(1,100), ".o%d" % random.randint(1,100)
        self.cleanup_dirs = [from_dir, to_dir]
        git = 'git'
        operations.create_repository(git, from_dir)
        result = operations.fork_repository(git, from_dir, to_dir)
        self.assertTrue(isinstance(result, bool))
        self.assertTrue(result)
        self.assertTrue(os.path.exists('/'.join([to_dir, 'config']))) 

class TestOfCreateRepository(TestCase):
    def setUp(self):
        self.mox = mox.Mox()
        self.cleanup_dirs = []

    def tearDown(self):
        self.mox.UnsetStubs()
        if self.cleanup_dirs:
            for dir in self.cleanup_dirs:
                shutil.rmtree(dir)

    def test_repo_already_exists(self):
        from_dir = ".%d" % random.randint(1,100)
        self.cleanup_dirs = [from_dir,]
        git = 'git'
        operations.create_repository(git, from_dir)
        self.assertRaises(KittyGitRepoExists, operations.create_repository, git, from_dir)

    def test_repo_creates_bare_by_default(self):
        from_dir = ".%d" % random.randint(1,100)
        self.cleanup_dirs = [from_dir,]
        git = 'git'
        result = operations.create_repository(git, from_dir)
        time.sleep(1)
        self.assertTrue(os.path.exists(os.path.join(from_dir, 'config')))

    def test_repo_can_create_non_bare(self):
        from_dir = ".%d" % random.randint(1,100)
        self.cleanup_dirs = [from_dir,]
        git = 'git'
        result = operations.create_repository(git, from_dir, bare=False)
        time.sleep(1)
        self.assertTrue(os.path.exists(os.path.join(from_dir, '.git/config')))

    def test_repo_can_create_with_templates(self):
        from_dir = ".%d" % random.randint(1,100)
        self.cleanup_dirs = [from_dir,]
        git = 'git'
        result = operations.create_repository(git, from_dir, 'tests/support')
        hook_path = os.path.join(from_dir, 'hooks/post-commit')
        orig_path = 'tests/support/hooks/post-commit'
        self.assertTrue(os.path.exists(hook_path))
        lhs, rhs = open(hook_path, 'r'), open(orig_path, 'r')
        lhs_results, rhs_results = lhs.read(), rhs.read()
        self.assertEqual(lhs_results, rhs_results)
        lhs.close(); rhs.close()

