def save_figures(name,format):
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    '''
    Save figures to individual numbered graphics files
    
    INPUTS:
    name   : name of graphic file, e.g. Dynamic Kundur
    format : graphics file format supported by matplotlib savefig, e.g. '.png'
    
    OUTPUTS:
    None
    
    EXAMPLE:
    _save_figures('example1','.png')
    '''
    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums]
    if (format == '.pdf'):
        pdfFile = name + format
        pp = PdfPages(pdfFile)
        for fig in figs:
            fig.savefig(pp, format='pdf')
        pp.close()
    else:
        if len(figs) == 1:
            figs[0].savefig(name + format)
        else:
            ifig = 1
            for fig in figs:
                fig.savefig(name + '_' + str(ifig) + format)
                ifig += 1
    
    return 
