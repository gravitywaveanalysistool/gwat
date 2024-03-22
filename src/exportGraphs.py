"""
- This function requires a list of desired graphs to be input which should be passed from the UI
when the user checks off the graphs they want to export
- Graphs will then be exported to a single pdf file
- Defaults to pdf but further file types can be added later if needed
"""

from matplotlib.backends.backend_pdf import PdfPages


# Talk to Eric to see how he's handling the desired graphs from UI
def exportGraphs(graphs, filePath):
    outputFile = PdfPages(filePath)  # Creates the output file
    for graph in graphs:  # Saves each graph to file
        graph.savefig(outputFile, format='pdf')
    outputFile.close()
