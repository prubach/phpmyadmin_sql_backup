#!/usr/bin/env python3
import argparse
import os
import re
import sys
import datetime
import mechanize

__version__ = '2025-04-06'
CONTENT_DISPOSITION_FILENAME_RE = re.compile(r'^.*filename="(?P<filename>[^"]+)".*$')
DEFAULT_PREFIX_FORMAT = r'%Y%m%d_%H%M%S_'

def create_browser():
    br = mechanize.Browser()
    # Ignore robots.txt
    br.set_handle_robots(False)
    return br

def do_login(br, url, username, password, server):
    # Login page
    br.open(url)

    # Fill login form
    br.select_form('login_form')
    br['pma_username'] = username
    br['pma_password'] = password
    if server is not None:
        br['pma_servername'] = server

    # Login and check if logged in
    response = br.submit()
    return response

def get_world_sql_path():
    if os.path.exists('/world.sql'):
        return '/world.sql'
    elif os.path.exists('./world.sql'):
        return './world.sql'
    else:
        path = os.path.dirname(os.path.realpath(__file__))
        return path + '/world.sql'


def export_to_folder(url, user, password, dry_run=False, overwrite_existing=False, prepend_date=True, basename=None,
                        output_directory=os.getcwd(), exclude_dbs=None, compression='none', prefix_format=None,
                        timeout=60, http_auth=None, server_name=None, **kwargs):

    prefix_format = prefix_format or DEFAULT_PREFIX_FORMAT
    exclude_dbs = exclude_dbs.split(',') or []
    encoding = '' if compression == 'gzip' else 'gzip'

    save_dir = output_directory

    br = create_browser()

    response = do_login(br, url, user, password, server_name)

    assert(b'Server version' in response.read())

    # Open server export
    response = br.follow_link(text_regex=re.compile('Export'))
    response = response.read()
    br.select_form('dump')

    if compression != 'none':
        item = br.find_control('compression').get(compression)
        item.selected = True
    response = br.submit()

    re_match = CONTENT_DISPOSITION_FILENAME_RE.match(response.headers['Content-Disposition'])
    if not re_match:
        raise ValueError(
            'Could not determine SQL backup filename from {}'.format(response.headers['Content-Disposition']))

    content_filename = re_match.group('filename')
    filename = content_filename if basename is None else basename + os.path.splitext(content_filename)[1]

    if prepend_date:
        prefix = datetime.datetime.now().strftime(prefix_format)
        filename = prefix + filename
    out_filename = os.path.join(output_directory, filename)

    if os.path.isfile(out_filename) and not overwrite_existing:
        basename, ext = os.path.splitext(out_filename)
        n = 1
        print('File {} already exists, to overwrite it use --overwrite-existing'.format(out_filename), file=sys.stderr)
        while True:
            alternate_out_filename = '{}_({}){}'.format(basename, n, ext)
            if not os.path.isfile(alternate_out_filename):
                out_filename = alternate_out_filename
                break
            n += 1

    file_content = response.read()
    with open(out_filename, 'wb') as file:
        file.write(file_content)
    return out_filename


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Automates the download of SQL dump backups via a phpMyAdmin web interface. Based on https://github.com/phpmyadmin/docker/blob/master/testing/phpmyadmin_test.py',
        epilog='Program options from: https://github.com/qubitstream/phpmyadmin_sql_backup, by Pawel Rubach version: {}'.format(__version__))

    parser.add_argument('url', metavar='URL', help='phpMyAdmin login page url')
    parser.add_argument('user', metavar='USERNAME', help='phpMyAdmin login username')
    parser.add_argument('password', metavar='PASSWORD', help='phpMyAdmin login password')
    parser.add_argument('-o', '--output-directory', default=os.getcwd(),
                        help='output directory for the SQL dump file (default: the current working directory)')
    parser.add_argument('-p', '--prepend-date', action='store_true', default=False,
                        help='prepend current UTC date & time to the filename; '
                             'see the --prefix-format option for custom formatting')
    parser.add_argument('-e', '--exclude-dbs', default='',
                        help='comma-separated list of database names to exclude from the dump')
    parser.add_argument('-s', '--server-name', default=None,
                        help='mysql server hostname to supply if enabled as field on login page')
    parser.add_argument('-c', '--compression', default='none', choices=['none', 'zip', 'gzip'],
                        help='compression method for the output file - must be supported by the server (default: %(default)s)')
    parser.add_argument('--basename', default=None,
                        help='the desired basename (without extension) of the SQL dump file (default: dump'
                             '); you can also set an empty basename "" in combination with '
                             '--prepend-date and --prefix-format')
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help='do not print any output')
    parser.add_argument('--timeout', type=int, default=60,
                        help='timeout in seconds for the requests (default: %(default)s)')
    parser.add_argument('--overwrite-existing', action='store_true', default=False,
                        help='overwrite existing SQL dump files (instead of appending a number to the name)')
    parser.add_argument('--prefix-format', default='',
                        help=str('the prefix format for --prepend-date (default: "{}"); in Python\'s strftime format. '
                                 'Must be used with --prepend-date to be in effect'.format(
                            DEFAULT_PREFIX_FORMAT.replace('%', '%%'))))
    parser.add_argument('--dry-run', action='store_true', default=False,
                        help='dry run, do not actually download any file')
    parser.add_argument('--http-auth', default=None,
                        help='Basic HTTP authentication, using format "username:password"')

    args = parser.parse_args()

    if args.prefix_format and not args.prepend_date:
        print('Error: --prefix-format given without --prepend-date', file=sys.stderr)
        sys.exit(2)

    try:
        dump_fn = export_to_folder(**vars(args))
    except Exception as e:
        print('Error: {}'.format(e), file=sys.stderr)
        sys.exit(1)

    if not args.quiet:
        print('{} saved SQL dump to: {}'.format(('Would have' if args.dry_run else 'Successfully'), dump_fn),
          file=sys.stdout)
