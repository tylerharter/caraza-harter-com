# Reading: Reproducibility 2

As data scientists, we want our work to be reproducible.  If somebody
else runs our analysis code, they ought to get the same result we got.

Using different version of the same package can break reproducibility.
If I am using version 1.1.0 of pandas, and you are using version
1.2.0, we might get different results, even if we're running the same
code.  Versions of a package are called *releases*.

**Note:** if you want to try the examples here for yourself, you'll
  need to wait until you setup your Linux virtual machine in lab next
  week, then use that.

## Package Releases

`pip install somepackage` (some systems use `pip3`) will install the
latest version of `somepackage` (unless another version has already
been installed.  If you want a specific version, you can run something
like `pip install somepackage==1.2.3`.

If reproducibility is very important, it's common to require other
people running your code to install specific versions of the relevant
packages.  `venv` (not covered in 320) is a popular tool for making it
easier to impose such requirements:
https://docs.python.org/3/library/venv.html#creating-virtual-environments

Running `pip install` downloads and installs packages from PyPI
(https://pypi.org/), a package index where anybody can publish their
packages.  The developers that publish to PyPI will typically store
their code (including versions not yet released to PyPI) using a
version-control tool, described next.

## Version Control Systems (VCS)

Version control systems allow developers to store not only the code
for a project, but a history of changes to that code.  Generally,
developers take snapshots of the code at specific points in time,
typically with a brief message describing what has changed.  This
allows teams to look back at who has contributed what and also
rollback buggy versions.

Generally, only a small subset of snapshots will get published as a
release on an index like PyPI.  A new feature might have many
milestones along the way, but you wouldn't want to officially release
it someplace like PyPI until the feature is complete.

There are many examples of VCS tools, such as svn, TeamFoundation,
Mercurial, and git.  We'll learn git, an open-source tool developed by
Linus Torvalds (also creator of Linux) in this course.  You can run
git directly yourself, but there are also a number of companies that
provide git hosting as a service (often with a free tier); some of the
services include GitLab, BitBucket, and GitHub.  We'll learn GitHub.

## Git

In git, a snapshot of the files in a project is called a *commit*.  In
the simplest case, git records history as a sequence of commits.  Git
can record this history in a *repository* ("repo" for short), a
special *directory* (informally called a "folder") on your computer.
This is convenient, because whenever you're in that directory, you're
looking at one version of the files (often the latest).  The other
commits are stored as hidden files, and there are special git commands
to see those.  Repositories can also be hosted on GitHub.

### Repos

There are two ways to create a repo on your computer: (1) copy it down from
a host, like GitHub, or (2) make an empty one.

Copying from a site like GitHub can be done with the `clone` command.
Take a look at this repo: https://github.com/tylerharter/cs320-p1.
Now, click on the "Code" button, then click "HTTPS", and copy the URL:

<img src="img/clone.png" width=300>

Now, open a terminal, `cd` to a directory where you can do some scratch work, and run the following:

`git clone https://github.com/tylerharter/cs320-p1.git`

This will create a directory called `cs320-p1`.  `cd` into it, then
run `ls -a` ("ls" means list files, and the "-a" flags means show them
all, including hidden files).  You'll see this:

```
.	..	.git	wc.py
```

`wc.py` is an example of a file in this repo (in its latest form), and
`.git` contains prior commits with other versions of that file.

Run `git log`.  You'll see something like this:

```
commit 4e4128313b8d5b5e5d04f2e8e585f64f7c5831a4 (HEAD -> main, origin/main, origin/HEAD)
Author: Steve <steve@example.com>
Date:   Mon Jan 20 15:00:00 2020 -0600

    only make one pass over list to count all

commit f637df3f45bc389e1035cc3aadcf5d81a55f0dc4
Author: Steve <steve@example.com>
Date:   Sat Jan 18 18:00:00 2020 -0600

    only make one pass over list to count all

commit c10b5a6cb4f06c96f6f221df2d5ec33af767d5c5
Author: Ada <ada@example.com>
Date:   Thu Jan 16 13:00:00 2020 -0600

    optimize: only compute count once per unique word
...
```

Each commit represents a version of the code.  You can also see the
author, date, and commit message.  Let's take a look at this version
of the code, switch to another commit, then look at that version of the code.

```
cat wc.py
git checkout 6d7beafb8e79b7a92fed8e67673a33bb7f607dbe
cat wc.py
```

The `checkout` command is for changing versions, and
"b0df6dbe111f9e28fc3a9c9b841cde5c20c365f9" is an example of a commit
number.  It contains letters, because it is *hexadecimal*, meaning it
contains 16 digits ("decimal" digits that we're familiar with include
0-9, "binary" digits include 0 and 1, and hexadecimal digits include
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F).

If you run `git log` again, you'll notice the command only shows the
history prior to the commit you're currently on.  You can run `git
checkout main` to jump back to the latest commit.

You can also create a repo from scratch, not associated with anything
on GitHub.  Let's try that now:

```
cd ..
mkdir fresh
cd fresh
git init
```

Here, we named the new repo "fresh", but you could have called it anything.

### Creating Commits

Before we can create commits in our new repo, we need to create some
files.  You could do this with any tool you like (e.g., you could run
Jupyter in this directory).  `nano` is a simple terminal-editor you
may want to learn (https://itsfoss.com/nano-editor-guide/).

Create a file in the directory called "x.txt" that contains the
word "apple".  Now, run `git status`.  You'll see something like this:

```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	x.txt
```

We'll follow the hint and run `git add x.txt`.  If you run the status
command again, you'll see the new file is ready to be committed:

```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   x.txt
```

Now we can create a commit using the `commit` command, as well as specify a string message using the `-m` flag:

```
git commit -m 'say whatever you want here about your work'
```

If this is your first time using git on this computer, it might
complain it doesn't know who you are (remember that git remembers who
made what changes).  You can tell it with commands like these:

```
git config -- global user.email "PUT YOUR EMAIL HERE"
git config -- global user.name "PUT YOUR NAME HERE"
```

Run `git status` and `git log` to get a sense of your current workspace (you'll run those a lot).

Now do two things:
1. change "x.txt" so that it contains "banana"
2. create a "y.txt" file that contains "cabbage"

Run `git status`, and you'll see something like this:

```
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   x.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	y.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

Note how git is suggesting `git add` for both our files.  Files can
either be "untracked" (new files), "not staged" (prior files that have
been modified), or "staged" (files that have been added since the last
change).  Only staged files get committed, and (somewhat annoyingly)
you'll need to re-add the same file each time you want to snapshot it
as part of a new commit.  So run `git add x.txt y.txt` to stage both
files, check the `git status` again, then create another commit, with
a message of your choosing.  If you run `git log` again, you'll see
both your commits:

```
commit 083dc3e19511f8c0b4ec24661fbb40df6e963335 (HEAD -> main)
Author: tylerharter <tylerharter@gmail.com>
Date:   Tue Jan 12 18:09:55 2021 -0600

    more fruits

commit f8e8858108860cd02a78776d1abcdd7a796d9480
Author: tylerharter <tylerharter@gmail.com>
Date:   Tue Jan 12 18:02:02 2021 -0600

    create the apple file
```

If you switch to the first commit (using a `git checkout`), then run
"ls", you'll only see the x.txt file.  If you switch back to the
latest commit, you'll see both.

## Summary of Concepts and Commands

**Concepts:** version control, snapshot, release, staged, tracked.

**Git Commands:** clone, init, add, commit, checkout, log, status.
