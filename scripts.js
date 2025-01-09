// Load and process the analysis results
console.log('Loading analysis results...');
const currentUrl = window.location.href;
const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/') + 1);
fetch(baseUrl + 'analysis_results.json', {
    headers: {
        'Accept': 'application/json'
    }
})
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Analysis results loaded successfully');
        populateSummaryStats(data);
        createVariantTypeChart(data);
        createAlleleFrequencyHistogram(data);
        createChromosomeDistribution(data);
        initializeVariantTable(data);
    })
    .catch(error => {
        console.error('Error loading analysis results:', error);
        document.getElementById('summary-stats').innerHTML = '<p class="error">Error loading analysis data. Please check the console for details.</p>';
    });

function populateSummaryStats(data) {
    const summaryHtml = `
        <div class="stat-box">
            <div class="stat-value">${data.total_variants.toLocaleString()}</div>
            <div class="stat-label">Total Variants</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">${data.snp_count.toLocaleString()}</div>
            <div class="stat-label">SNPs (${data.snp_percentage.toFixed(1)}%)</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">${data.indel_count.toLocaleString()}</div>
            <div class="stat-label">Indels (${data.indel_percentage.toFixed(1)}%)</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">${data.most_common_chromosome}</div>
            <div class="stat-label">Most Common Chromosome</div>
        </div>
    `;
    document.getElementById('summary-stats').innerHTML = summaryHtml;
}

function createVariantTypeChart(data) {
    const ctx = document.getElementById('variantTypeChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['SNPs', 'Indels'],
            datasets: [{
                data: [data.snp_count, data.indel_count],
                backgroundColor: ['#007bff', '#28a745']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Variant Type Distribution'
            }
        }
    });
}

function createAlleleFrequencyHistogram(data) {
    const labels = Object.keys(data.af_histogram);
    const values = Object.values(data.af_histogram);
    
    const ctx = document.getElementById('afHistogram').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Frequency',
                data: values,
                backgroundColor: '#17a2b8'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Allele Frequency Distribution'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Number of Variants'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Allele Frequency Range'
                    }
                }]
            }
        }
    });
}

function createChromosomeDistribution(data) {
    const chromosomes = Object.keys(data.chromosome_counts);
    const counts = Object.values(data.chromosome_counts);
    
    const ctx = document.getElementById('chromosomeDistribution').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chromosomes,
            datasets: [{
                label: 'Variants per Chromosome',
                data: counts,
                backgroundColor: '#fd7e14'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Variants per Chromosome'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Number of Variants'
                    }
                }]
            }
        }
    });
}

function initializeVariantTable(analysisData) {
    console.log('Loading variants table...');
    // Load variants from separate file
    fetch(baseUrl + 'variants.json', {
        headers: {
            'Accept': 'application/json'
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(variants => {
            console.log(`Loaded ${variants.length} variants, limiting to first 1000`);
            // Load the first 1000 variants for better performance
            const limitedVariants = variants.slice(0, 1000);
            
            $('#variantsTable').DataTable({
                data: limitedVariants,
                columns: [
                    { data: 'chrom', title: 'Chromosome' },
                    { data: 'pos', title: 'Position' },
                    { data: 'ref', title: 'Reference' },
                    { data: 'alt', title: 'Alternate' },
                    { 
                        data: 'af',
                        title: 'Allele Frequency',
                        render: function(data) {
                            return data ? data.toFixed(3) : '0.000';
                        }
                    },
                    { data: 'dp', title: 'Read Depth' },
                    { 
                        data: 'qual',
                        title: 'Quality',
                        render: function(data) {
                            return data ? data.toFixed(1) : '0.0';
                        }
                    },
                    {
                        data: 'clinvar_significance',
                        title: 'ClinVar Significance',
                        render: function(data) {
                            return data || 'Unknown';
                        }
                    }
                ],
                pageLength: 25,
                order: [[0, 'asc'], [1, 'asc']],
                dom: 'Bfrtip',
                buttons: ['copy', 'csv', 'excel'],
                scrollX: true,
                processing: true
            });
        })
        .catch(error => {
            console.error('Error loading variants:', error);
            document.getElementById('variant-table').innerHTML += '<p class="error">Error loading variant data. Please check the console for details.</p>';
        });
}
