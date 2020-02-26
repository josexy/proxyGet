#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from proxyPool import TestProxyPool,asyncTestProxyPool
from proxyMessage import CliMessage,Color
from proxyOption import HelpPanel
import proxy_config

def main(help_panel):
    # examples:
    # proxyGet.py --help
    # proxyGet.py -0 -5
    # proxyGet.py -3 -7 --async
    # proxyGet.py -0 -7 -m 10 -t 5 --mysql --host=127.0.0.1 --port=3306 -u root -p xxx --database=db_proxy --table=tb_proxy
    # proxyGet.py -1 -5 --async --max=2 --timeout=3 --retry=1 --file=db/test.db --table=tb_proxy --from=2 --to=4
    from_page_index=help_panel['from_page_index']
    to_page_index=help_panel['to_page_index']
    if from_page_index <= 0 or to_page_index <= 0 or from_page_index > to_page_index:
        CliMessage.print_with_status('Page index is invalid',Color.Red,Color.Bold,None,'failed')
        exit(0)

    col = help_panel.collect(help_panel.url)
    if help_panel['_async']:
        CliMessage.print_with_status('Currently you have selected an asynchronous operation to obtain the proxy',Color.Green)
        testpool=asyncTestProxyPool(col.table_field(),help_panel.optionBox)
    else:
        testpool=TestProxyPool(col.table_field(),help_panel.optionBox)
    for page_index in range(from_page_index,to_page_index+1):
        # set new page index
        col.set_page_index(page_index)
        for per_proxy in col.run():
            if not testpool.add_ip(per_proxy):
                break
        try:
            testpool.start_test()
        except:
            break
        if page_index!=to_page_index:
            CliMessage.print_with_status('Next Page...')

if __name__ == '__main__':
    proxy_config.OUTPUT_DEBUG_INFO=True
    help_panel=HelpPanel()
    main(help_panel)

