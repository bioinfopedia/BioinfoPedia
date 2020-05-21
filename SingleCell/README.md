# Single Cell Project Plans

Long term	:	Web server to help analyze single cell data from .fastq files
Short term	: 	Docker image that can be pulled for analysis on local machines

## Workflow

1. Generate **Raw QC Report** on user-provided raw data.
2. Check if input file is large (Determine read threshold). If yes, break into subsamples and **Pre-process** subsamples (sequentially/parallelly) based on input parameters (Eg: Adapter sequence, Quality Threshold), collate, and store results in the user-provided Path.
3. Generate **Pre-processed QC Report** on pre-processed data. Provide comparison with raw data QC report.
4. Provide options to **Repeat Pre-processing** and save results in a different folder.
5. Generate **Feauture-Barcode Matrix** following alignment.
6. Post-processing using Seurat or a custom script using Autoencoders to improve clustering efficiency (To be discussed in detail)




