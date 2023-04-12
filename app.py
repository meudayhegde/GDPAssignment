#!/usr/bin/python3

import logging

from utils import safe_import_attr
from DBUtil import DBUtil

Flask, render_template, send_file, send_from_directory, redirect, url_for, request, make_response = safe_import_attr(
    'flask', 'Flask', 'render_template', 'send_file', 'send_from_directory', 'redirect', 'url_for', 'request',
    'make_response')


class GDPServer:

    def __init__(self, db_util: DBUtil, port: int, host: str, debug=True):
        self.app = Flask(__name__)
        self.db_util = db_util
        self.set_config(PORT=port, HOST=host)
        self.debug = debug
        self.log = logging.getLogger('gdpwebserver')
        self.create_routes()

    def set_config(self, **varargs):
        for key, value in varargs.items():
            self.app.config[key] = value

    def create_routes(self):
        @self.app.route('/')
        def home():
            return redirect(url_for('usd'))

        @self.app.route('/usd')
        def usd():
            gdp = self.db_util.get_all_gdp_entries()
            labels = [str(key) for key in gdp.keys()]
            varargs = {
                'title': f'GDP of India {labels[0]}-{labels[-1]}',
                'content_title': f'India: Gross domestic product (GDP) in current prices from {labels[0]} to {labels[-1]}',
                'labels': labels,
                'values': gdp.values(),
                'unit': 'USD Billions',
                'button': 'change data unit to INR',
                'button_redirect': 'inr'
            }
            return render_template('chart.html', **varargs)

        @self.app.route('/inr')
        def inr():
            gdp = self.db_util.get_all_gdp_entries()
            usd_conv = self.db_util.get_all_usd_entries()
            labels = list(gdp.keys())

            varargs = {
                'title': f'GDP of India {labels[0]}-{labels[-1]}',
                'content_title': f'India: Gross domestic product (GDP) in current prices from {labels[0]} to {labels[-1]}',
                'labels': [str(key) for key in labels],
                'values': [gdp[year] * usd_conv[year] for year in labels],
                'unit': 'INR Billions',
                'button': 'change data unit to USD',
                'button_redirect': 'usd'
            }
            return render_template('chart.html', **varargs)

    def start(self):
        self.app.run(debug=self.debug, host=self.app.config['HOST'], port=self.app.config['PORT'])
