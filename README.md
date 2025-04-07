# phpmyadmin_sql_backup.py

New version based on: https://github.com/phpmyadmin/docker/blob/master/testing/phpmyadmin_test.py

## What is it?

A Python 3 script to __automate the download of SQL backups via a 
[phpMyAdmin](https://www.phpmyadmin.net/) web interface__.

This is useful when your web hosting provider does not grant you access to a console (for `mysqldump`) but
you want to automate the backup of your database (without having to manually use the browser).

It has been tested with Python 3.12 on Linux and the following versions of phpMyAdmin:
`5.2.x` 

_Note_: The web interface of phpMyAdmin may change in the future and break this script. Please file a bug report
(including your version of phpMyAdmin) if you encounter this issue.

## Usage

    usage: phpmyadmin_sql_backup.py [-h] [-o OUTPUT_DIRECTORY] [-p]
                                    [-e EXCLUDE_DBS] [-s SERVER_NAME]
                                    [--compression {none,zip,gzip}]
                                    [--basename BASENAME] [--timeout TIMEOUT]
                                    [--overwrite-existing]
                                    [--prefix-format PREFIX_FORMAT] [--dry-run]
                                    [--http-auth HTTP_AUTH]
                                    URL USERNAME PASSWORD
    
    Automates the download of SQL dump backups via a phpMyAdmin web interface.
    
    positional arguments:
      URL                   phpMyAdmin login page url
      USERNAME              phpMyAdmin login username
      PASSWORD              phpMyAdmin login password
    
    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                            output directory for the SQL dump file (default: the
                            current working directory)
      -p, --prepend-date    prepend current UTC date & time to the filename; see
                            the --prefix-format option for custom formatting
      -e EXCLUDE_DBS, --exclude-dbs EXCLUDE_DBS
                            comma-separated list of database names to exclude from
                            the dump
      -s SERVER_NAME, --server-name SERVER_NAME
                            mysql server hostname to supply if enabled as field on
                            login page
      --compression {none,zip,gzip}
                            compression method for the output file - must be
                            supported by the server (default: none)
      --basename BASENAME   the desired basename (without extension) of the SQL
                            dump file (default: the name given by phpMyAdmin); you
                            can also set an empty basename "" in combination with
                            --prepend-date and --prefix-format
      --timeout TIMEOUT     timeout in seconds for the requests (default: 60)
      --overwrite-existing  overwrite existing SQL dump files (instead of
                            appending a number to the name)
      --prefix-format PREFIX_FORMAT
                            the prefix format for --prepend-date (default:
                            "%Y-%m-%d--%H-%M-%S-UTC_"); in Python's strftime
                            format. Must be used with --prepend-date to be in
                            effect
      --dry-run             dry run, do not actually download any file
      --http-auth HTTP_AUTH
                            Basic HTTP authentication, using format
                            "username:password"
    
    Written by Christoph Haunschmidt et al., version: 2019-05-07.1

### Examples

    phpmyadmin_sql_backup.py "http://www.example.com/phpmyadmin/" your_user your_password

Downloads a plain text `.sql` backup of all databases to the current working directory.

---

    phpmyadmin_sql_backup.py "http://www.example.com/phpmyadmin/" your_user your_password --exclude-dbs mydb2,mydb4 --prepend-date --basename example_dump --output-directory /tmp --compression zip

Downloads a zipped dump with databases `mydb2` & `mydb4` excluded, the base name `example_dump` and a prepended
UTC date / time to the directory `/tmp`, e.g. `/tmp/2016-03-11--15-19-04-UTC_example_dump.zip`.

## Requirements

 - A [Python 3.12](https://www.python.org/) installation on your system
 - mechanize

## License

[GNU GPL3](https://www.gnu.org/licenses/gpl-3.0.html)

## Contributors

 - Pawel Rubach (new version based on https://github.com/phpmyadmin/docker/blob/master/testing/phpmyadmin_test.py)
 - Christoph Haunschmidt (original author)
 - Jason Harper (optional mysql server hostname)
 - Jonas Bengtsson (older frame-based phpMyAdmin support)
 - Benoît Courtine (HTTP Auth)
 
 
