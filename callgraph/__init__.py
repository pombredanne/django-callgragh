import time
from pycallgraph import Config
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph.globbing_filter import GlobbingFilter
from django.conf import settings


def create_graph(output_type='dot'):
    '''
    starts the graph call. Keep the returned object and run done() on it to finish the graph creation.
    '''

    config = Config()
    config.trace_filter = GlobbingFilter(exclude=['pycallgraph.*', 'django.core.*', 'collections.*', 'copy.*',
                                                  'threading.*', 'logging.*', 'multiprocessing.*', 'inspect.*',
                                                  'string.*', 'Cookie.*', 'importlib.*', 'pdb.*', 'shutil.*',
                                                  're.*', 'os.*', 'sys.*', 'json.*', 'decimal.*', 'urllib.*',
                                                  ])

    output_type = 'dot'
    output_file = 'tccallgraph-{}.{}'.format(str(time.time()), output_type)
    graphviz = GraphvizOutput(output_file=output_file, output_type=output_type)
    pycallgraph = PyCallGraph(output=graphviz, config=config)
    pycallgraph.start(reset=True)

    return pycallgraph


class CallgraphMiddleware(object):

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if settings.GRAPH_CALL and 'graph' in request.GET:
            self.pycallgraph = create_graph(output_type='dot')

    def process_response(self, request, response):
        if settings.GRAPH_CALL and 'graph' in request.GET:
            self.pycallgraph.done()
        return response
