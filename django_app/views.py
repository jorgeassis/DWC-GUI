import random, json
import pandas as pd

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import speciesRecords, biodiversityRecords
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from django.db.models import Q # new
from django.http import HttpResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import numpy as np

import random
from django.db.models import Count

# ----------
# View and Search engine [Records - Table and Map]

def recordsView(request):
    
    recordsAll = biodiversityRecords.objects.all()
    speciesAll = speciesRecords.objects.all()
    
    query = 'None'

    # [1] Simple Search
    if request.GET.get('searchType') == None:

        searchType = None

        query = request.GET.get('q')
        if query:
            recordsAll = recordsAll.filter(
                Q(scientificName__icontains=query) | Q(locality__iexact=query) | Q(bibliographicCitation__icontains=query)
            )
        query = request.GET.get('id')
        if query:
            recordsAll = recordsAll.filter(
                Q(pk__in=query)
            )

    # [2] Advanced Search
    if request.GET.get('searchType') == 'Advanced':

        searchType = 'Advanced'
        searchRelateSpecies = False

        # [2.1] Species queries
        if request.GET.get('conservationIUCNGlobal') != '':
            querySP = request.GET.get('conservationIUCNGlobal')
            if querySP:
                speciesAll = speciesAll.filter(
                    Q(conservationIUCNGlobal__iexact=querySP)
                )
                searchRelateSpecies = True
        if request.GET.get('conservationIUCNEurope') != '':
            querySP = request.GET.get('conservationIUCNEurope')
            if querySP:
                speciesAll = speciesAll.filter(
                    Q(conservationIUCNEurope__iexact=querySP)
                )
                searchRelateSpecies = True
        if request.GET.get('conservationRedBookPt') != '':
            querySP = request.GET.get('conservationRedBookPt')
            if querySP:
                speciesAll = speciesAll.filter(
                    Q(conservationRedBookPt__iexact=querySP)
                )
                searchRelateSpecies = True
        if request.GET.get('conservationN2000') != '':
            querySP = request.GET.get('conservationN2000')
            if querySP:
                speciesAll = speciesAll.filter(
                    Q(conservationN2000__iexact=querySP)
                )
                searchRelateSpecies = True

        if searchRelateSpecies:
            speciesAll = speciesAll.values('scientificName')
            recordsAll = recordsAll.filter(Q(scientificName__in=speciesAll))

        # [2.2] Record queries
        if request.GET.get('bibliographicCitation') != '':
            query = request.GET.get('bibliographicCitation')
            if query:
                recordsAll = recordsAll.filter(
                    Q(bibliographicCitation__icontains=query)
                )
        if request.GET.get('bibliographicCitationExact') != '':
            query = request.GET.get('bibliographicCitationExact')
            if query:
                recordsAll = recordsAll.filter(bibliographicCitation=query)
        if request.GET.get('scientificName') != '':
            query = request.GET.get('scientificName')
            if query:
                recordsAll = recordsAll.filter(
                    Q(scientificName__icontains=query)
                )
        if request.GET.get('locality') != '':
            query = request.GET.get('locality')
            if query:
                recordsAll = recordsAll.filter(
                    Q(locality__icontains=query)
                )
        if request.GET.get('yearTo') != '':
            query = request.GET.get('yearTo')
            if query:
                recordsAll = recordsAll.filter(
                    Q(year__lte=query)
                )
        if request.GET.get('yearFrom') != '':
            query = request.GET.get('yearFrom')
            if query:
                recordsAll = recordsAll.filter(
                    Q(year__gte=query)
                )
        if request.GET.get('monthTo') != '':
            query = request.GET.get('monthTo')
            if query:
                recordsAll = recordsAll.filter(
                    Q(month__lte=query)
                )
        if request.GET.get('monthFrom') != '':
            query = request.GET.get('monthFrom')
            if query:
                recordsAll = recordsAll.filter(
                    Q(month__gte=query)
                )
        if request.GET.get('depthTo') != '':
            query = request.GET.get('depthTo')
            if query:
                recordsAll = recordsAll.filter(
                    Q(verbatimDepth__lte=query)
                )
        if request.GET.get('depthFrom') != '':
            query = request.GET.get('depthFrom')
            if query:
                recordsAll = recordsAll.filter(
                    Q(verbatimDepth__gte=query)
                )          
        if request.GET.get('basisOfRecord') != '':
            query = request.GET.get('basisOfRecord')
            if query:
                recordsAll = recordsAll.filter(
                    Q(basisOfRecord__iexact=query)
                ) 
        if request.GET.get('associatedMedia') != '':
            query = request.GET.get('associatedMedia')
            if query:
                recordsAll = recordsAll.filter(
                    ~Q(associatedMedia__iexact=None)
                )               
        if request.GET.get('taxon') == 'Kingdom':
            query = request.GET.get('taxonName')
            if query:
                recordsAll = recordsAll.filter(
                    Q(Kingdom__iexact=query)
                )
        if request.GET.get('taxon') == 'Phylum':
            query = request.GET.get('taxonName')
            if query:
                recordsAll = recordsAll.filter(
                    Q(Phylum__iexact=query)
                )
        if request.GET.get('taxon') == 'Class':
            query = request.GET.get('taxonName')
            if query:
                recordsAll = recordsAll.filter(
                    Q(Class__iexact=query)
                )
        if request.GET.get('taxon') == 'Order':
            query = request.GET.get('taxonName')
            if query:
                recordsAll = recordsAll.filter(
                    Q(Order__iexact=query)
                )
        if request.GET.get('taxon') == 'Family':
            query = request.GET.get('taxonName')
            if query:
                recordsAll = recordsAll.filter(
                    Q(Family__iexact=query)
                )
        if request.GET.get('taxon') == 'Genus':
            query = request.GET.get('taxonName')
            if query:
                recordsAll = recordsAll.filter(
                    Q(Genus__iexact=query)
                )
        if request.GET.get('taxon') == 'Species':
            query = request.GET.get('taxonName')
            if query:
                recordsAll = recordsAll.filter(
                    Q(scientificName__iexact=query)
                )

    recordsCount = len(recordsAll)

    # Graph & Summary Data
    datasetCount = list(recordsAll.values_list('datasetName', flat=True).distinct())
    datasetCount = len(datasetCount)

    bibliographicCitationCount = list(recordsAll.filter( Q(basisOfRecord__iexact='Literature') ).values_list('bibliographicCitation', flat=True).distinct())
    bibliographicCitationCount = len(bibliographicCitationCount)

    recordsPerDataset = list(recordsAll.values('basisOfRecord').annotate(my_count=Count('id')))

    speciesArray = list(recordsAll.values_list('scientificName', flat=True).distinct())
    speciesCount = len(speciesArray)

    recordsWithMedia = list(recordsAll.filter( ~Q(associatedMedia__iexact=None) ).values_list('associatedMedia', flat=True).distinct())
    recordsWithMedia = len(recordsWithMedia)

    yearArray = list(recordsAll.values_list('year', flat=True))
    yearArray = list(filter(None, yearArray))

    recordsYearMin = None
    recordsYearMax = None
    recordsYearCount = None
    recordsPerYears = None
    recordsPerYearsX = None
    recordsPerMonth = None

    if len(yearArray) > 0:
        recordsYearMin = min(yearArray)
        recordsYearMax = max(yearArray)
        recordsYearCount = len(range(recordsYearMin,recordsYearMax))
        
        sliceYear = 6
        if recordsYearCount < 6:
            sliceYear = recordsYearCount + 1
        slicer = round(recordsYearCount/sliceYear)
        if slicer < 1:
            slicer = 1
        print(slicer)
        recordsPerYearsX = np.append(list(range(recordsYearMin,recordsYearMax))[::slicer],recordsYearMax)
        recordsPerYears = recordsAll.exclude(year__isnull=True).values('year').annotate(my_count=Count('id'))
        recordsPerYears = recordsPerYears.values("year", "my_count")

        df = pd.DataFrame.from_records(recordsPerYears)
        df['CumSum'] = np.cumsum(recordsPerYears.values_list('my_count', flat=True)).tolist() 
        recordsPerYearsX = list(df[df['year'].isin(recordsPerYearsX)]['year'])
        recordsPerYears = list(df[df['year'].isin(recordsPerYearsX)]['CumSum'])
        
        listOfMonths = list(range(1,13))
        recordsPerMonth = []

        for item in listOfMonths:
            res = list(recordsAll.filter(Q(month__iexact=item)).values('month').annotate(my_count=Count('id')).values_list('my_count', flat=True))
            if not res:
                recordsPerMonth.append(0)
            if res:
                recordsPerMonth.append(res[0])

    recordsPerType = recordsAll.exclude(basisOfRecord__isnull=True).values('basisOfRecord').annotate(my_count=Count('id'))

    recordsCount = recordsAll.count

    # Display type [Map / Table / Gallery]
    if request.GET.get('displayType') == 'Table':

            displayType = 'Table'

            page = request.GET.get('page', 1)
            paginator = Paginator(recordsAll, 25) # 25 posts per page
            page = request.GET.get('page')

            try:
                records = paginator.page(page)
            except PageNotAnInteger:
                records = paginator.page(1)
            except EmptyPage:
                records = paginator.page(paginator.num_pages)

            paginatorP = paginator.num_pages
            paginatorRange = paginator.page_range
            coordinates = None

    if request.GET.get('displayType') == 'Gallery':

            displayType = 'Gallery'
            recordsAll = recordsAll.filter(~Q(associatedMedia__iexact=None))    

            page = request.GET.get('page', 1)
            paginator = Paginator(recordsAll, 28) # 28 posts per page
            page = request.GET.get('page')

            try:
                records = paginator.page(page)
            except PageNotAnInteger:
                records = paginator.page(1)
            except EmptyPage:
                records = paginator.page(paginator.num_pages)

            paginatorP = paginator.num_pages
            paginatorRange = paginator.page_range
            coordinates = None

    if request.GET.get('displayType') == 'Map':

            displayType = 'Map'

            coordinates = list(recordsAll.values("decimalLongitude", "decimalLatitude","id"))
            coordinates = json.dumps(coordinates)
            records = None
            paginatorRange = None
            paginatorP = None

            
    mainTemplate = 'records.html'

    mydict = {
            
            'records':records, 
            'coordinates':coordinates, 

            'recordsCount':recordsCount,
            'paginatorRange':paginatorRange, 
            'paginatorP':paginatorP,

            'speciesCount':speciesCount,
            'recordsYearMin':recordsYearMin,
            'recordsYearMax':recordsYearMax,
            'recordsPerDataset':recordsPerDataset,
            'datasetCount':datasetCount,
            'bibliographicCitationCount':bibliographicCitationCount,
            'recordsYearCount':recordsYearCount,
            'recordsWithMedia':recordsWithMedia,
            'displayType':displayType,
            'searchType':searchType,

            'recordsPerYears':recordsPerYears,
            'recordsPerYearsX':recordsPerYearsX,
            'recordsPerMonth':recordsPerMonth,
            'recordsPerType':recordsPerType,
            'query':query
            }

    return render(request, mainTemplate, context=mydict)

# ----------
# View [record detail]

def recordsDetailView(request, id=None):
    
    record = get_object_or_404(biodiversityRecords, id=id)
    recordSpeciesName = record.scientificName

    speciesAll = speciesRecords.objects.all()
    
    speciesInfo = speciesAll.filter( Q(scientificName__iexact=recordSpeciesName) )
    speciesInfo = list(speciesInfo.values())

    context = {'record': record, 'speciesInfo': speciesInfo }
    return render(request, 'record-detail.html', context)

# ----------
# Simple View [record detail, no template]

def recordsDetailViewSimple(request, id=None):
    record = get_object_or_404(biodiversityRecords, id=id)
    context = {'record': record, }
    return render(request, 'record-detail-simple.html', context)

# ----------
# View [species]

from django.db.models import Max
from django.db.models import Min

def speciesView(request):
    
    recordsAll = biodiversityRecords.objects.all()
    
    speciesRecordsList = list(recordsAll.values_list('scientificName', flat=True).distinct())
    speciesRecordsListCount = len(speciesRecordsList)

    records = recordsAll.values('scientificName','Family','Genus').annotate(my_count=Count('id')).annotate(minYear=Min('year')).annotate(maxYear=Max('year'))

    page = request.GET.get('page', 1)
    paginator = Paginator(records, 25) # 25 species per page
    page = request.GET.get('page')

    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)

    paginatorP = paginator.num_pages
    paginatorRange = paginator.page_range

    mydict = {'speciesRecordsListCount':speciesRecordsListCount, 'records':records, 'paginatorRange':paginatorRange, 'paginatorP':paginatorP}
    return render(request, 'species.html', context=mydict)

# ----------
# View [literature]

def literatureView(request):
    
    recordsAll = biodiversityRecords.objects.all()
    recordsAll = recordsAll.filter(Q(basisOfRecord__iexact='Literature'))

    bibliographicRecordsList = list(recordsAll.values_list('bibliographicCitation', flat=True).distinct())
    bibliographicRecordsListCount = len(bibliographicRecordsList)

    records = recordsAll.values('bibliographicCitation').annotate(my_count=Count('id')).annotate(minYear=Min('year')).annotate(maxYear=Max('year'))

    page = request.GET.get('page', 1)
    paginator = Paginator(records, 25) # 25 species per page
    page = request.GET.get('page')

    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)

    paginatorP = paginator.num_pages
    paginatorRange = paginator.page_range

    mydict = {'bibliographicRecordsListCount':bibliographicRecordsListCount, 'records':records, 'paginatorRange':paginatorRange, 'paginatorP':paginatorP}
    return render(request, 'literature.html', context=mydict)

# ----------
# View [users]

def usersView(request):
    User = get_user_model()
    context = {
        'users': User.objects.all()
    }
    return render(request, 'users.html', context)

# ----------
# View [home]

def homeView(request):
    records = biodiversityRecords.objects.all()
    coordinates = list(records.values("decimalLongitude", "decimalLatitude","id"))
    
    # Random records from query
    coordinates = random.sample(coordinates, 10000)
    recordsCountSubset = 10000

    coordinates = json.dumps(coordinates)

    # Summary data
    speciesArray = list(records.values_list('scientificName', flat=True).distinct())
    yearArray = list(records.values_list('year', flat=True))
    yearArray = list(filter(None, yearArray))

    recordsYearMin = min(yearArray)
    recordsYearMax = max(yearArray)
    recordsYearCount = len(range(recordsYearMin,recordsYearMax)) # min(yearArray)
    recordsSpeciesCount = len(speciesArray)
    recordsCount = records.count()

    # Graph data
    recordsPerYearsX = np.append(list(range(recordsYearMin,recordsYearMax))[::round(recordsYearCount/6)],recordsYearMax)
    
    recordsPerYears = (records.exclude(year__isnull=True).values('year').annotate(my_count=Count('id')))
    recordsPerYears = recordsPerYears.values("year", "my_count")

    df = pd.DataFrame.from_records(recordsPerYears)
    df['CumSum'] = np.cumsum(recordsPerYears.values_list('my_count', flat=True)).tolist() 
    recordsPerYearsX = list(df[df['year'].isin(recordsPerYearsX)]['year'])
    recordsPerYears = list(df[df['year'].isin(recordsPerYearsX)]['CumSum'])
    
    recordsPerMonth = records.exclude(month__isnull=True).values('month').annotate(my_count=Count('id')).values_list('my_count', flat=True)

    recordsPerType = records.exclude(basisOfRecord__isnull=True).values('basisOfRecord').annotate(my_count=Count('id'))

    # Random pictures
    
    validIDs = records.filter(~Q(associatedMedia__iexact=None)).values_list('id', flat=True)
    randomValidIDs = random.sample(list(validIDs), 12)
    randomEntries = records.filter(id__in=randomValidIDs)

    mydict = {'randomEntries':randomEntries,'recordsPerType':recordsPerType, 'recordsPerMonth':recordsPerMonth, 'recordsPerYearsX':recordsPerYearsX, 'recordsPerYears':recordsPerYears, 'recordsYearMin':recordsYearMin, 'recordsYearMax':recordsYearMax, 'recordsYearCount':recordsYearCount, 'recordsSpeciesCount':recordsSpeciesCount, 'records':records, 'recordsCount':recordsCount, 'recordsCountSubset':recordsCountSubset, 'coordinates':coordinates}
    return render(request, 'home.html', context=mydict)

# ----------
# Download records by search criteria

def DownloadResultsView(request):
    recordsAll = biodiversityRecords.objects.all()
    mainTemplate = 'download-records.html'

    query = request.GET.get('q')
    if query:
        recordsAll = recordsAll.filter(
            Q(scientificName__iexact=query) | Q(locality__iexact=query) | Q(bibliographicCitation__icontains=query)
        )
    query = request.GET.get('bibliographicCitation')
    if query:
        recordsAll = recordsAll.filter(
            Q(bibliographicCitation__iexact=query)
        )
    query = request.GET.get('scientificName')
    if query:
        recordsAll = recordsAll.filter(
            Q(scientificName__iexact=query)
        )
    query = request.GET.get('locality')
    if query:
        recordsAll = recordsAll.filter(
            Q(locality__iexact=query)
        )
    query = request.GET.get('yearTo')
    if query:
        recordsAll = recordsAll.filter(
            Q(year__lte=query)
        )
    query = request.GET.get('yearFrom')
    if query:
        recordsAll = recordsAll.filter(
            Q(year__gte=query)
        )
    query = request.GET.get('monthTo')
    if query:
        recordsAll = recordsAll.filter(
            Q(month__lte=query)
        )
    query = request.GET.get('monthFrom')
    if query:
        recordsAll = recordsAll.filter(
            Q(month__gte=query)
        )
    query = request.GET.get('depthTo')
    if query:
        recordsAll = recordsAll.filter(
            Q(verbatimDepth__lte=query)
        )
    query = request.GET.get('depthFrom')
    if query:
        recordsAll = recordsAll.filter(
            Q(verbatimDepth__gte=query)
        )                    
    query = request.GET.get('basisOfRecord')
    if query:
        recordsAll = recordsAll.filter(
            Q(basisOfRecord__iexact=query)
        ) 
    query = request.GET.get('associatedMedia')
    if query:
        recordsAll = recordsAll.filter(
            ~Q(associatedMedia__iexact=None)
        )                     
    if request.GET.get('taxon') == 'Kingdom':
        query = request.GET.get('taxonName')
        if query:
            recordsAll = recordsAll.filter(
                Q(Kingdom__iexact=query)
            )
    if request.GET.get('taxon') == 'Phylum':
        query = request.GET.get('taxonName')
        if query:
            recordsAll = recordsAll.filter(
                Q(Phylum__iexact=query)
            )
    if request.GET.get('taxon') == 'Class':
        query = request.GET.get('taxonName')
        if query:
            recordsAll = recordsAll.filter(
                Q(Class__iexact=query)
            )
    if request.GET.get('taxon') == 'Order':
        query = request.GET.get('taxonName')
        if query:
            recordsAll = recordsAll.filter(
                Q(Order__iexact=query)
            )
    if request.GET.get('taxon') == 'Family':
        query = request.GET.get('taxonName')
        if query:
            recordsAll = recordsAll.filter(
                Q(Family__iexact=query)
            )
    if request.GET.get('taxon') == 'Genus':
        query = request.GET.get('taxonName')
        if query:
            recordsAll = recordsAll.filter(
                Q(Genus__iexact=query)
            )

    mydict = {'recordsAll':recordsAll }
    return render(request, mainTemplate, context=mydict)

# ----------
# Autocomplete engine

def search_autocomplete(request):
    if request.is_ajax():
        
        # All fields
        if request.GET.get('type') == 'All':
            query = request.GET.get('term', '')
            object_list = biodiversityRecords.objects.filter(
                Q(scientificName__icontains=query) | Q(locality__icontains=query) | Q(bibliographicCitation__icontains=query)
            )
            #places = biodiversityRecords.objects.filter(Q(scientificName__istartswith=query) | Q(locality__istartswith=query) | Q(Kingdom__istartswith=query) | Q(Phylum__istartswith=query) | Q(Class__istartswith=query) | Q(Order__istartswith=query) | Q(Family__istartswith=query) | Q(Genus__istartswith=query))
            #places = biodiversityRecords.objects.filter(scientificName__istartswith=query)
            results = []
            for pl in object_list:
                if str(query).lower() in str(pl.scientificName).lower():
                    results = results + [pl.scientificName]
                if str(query).lower() in str(pl.locality).lower():
                    results = results + [pl.locality]
                if str(query).lower() in str(pl.bibliographicCitation).lower():
                    results = results + [pl.bibliographicCitation]

        # Taxa field
        if request.GET.get('type') == 'Taxa':
            query = request.GET.get('term', '')
            object_list = biodiversityRecords.objects.filter(
                Q(scientificName__icontains=query) | Q(Genus__icontains=query) | Q(Family__icontains=query) | Q(Order__icontains=query) | Q(Class__icontains=query) | Q(Phylum__icontains=query)
            )
            results = []
            for pl in object_list:
                if str(query).lower() in str(pl.scientificName).lower():
                    results = results + [pl.scientificName]
                if str(query).lower() in str(pl.Genus).lower():
                    results = results + [pl.Genus]
                if str(query).lower() in str(pl.Family).lower():
                    results = results + [pl.Family]
                if str(query).lower() in str(pl.Order).lower():
                    results = results + [pl.Order]
                if str(query).lower() in str(pl.Class).lower():
                    results = results + [pl.Class]
                if str(query).lower() in str(pl.Phylum).lower():
                    results = results + [pl.Phylum_]

        # Site field
        if request.GET.get('type') == 'Site':
            query = request.GET.get('term', '')
            object_list = biodiversityRecords.objects.filter(
                Q(locality__icontains=query) 
            )
            results = []
            for pl in object_list:
                if str(query).lower() in str(pl.locality).lower():
                    results = results + [pl.locality]

        # Citation field
        if request.GET.get('type') == 'Citation':
            query = request.GET.get('term', '')
            object_list = biodiversityRecords.objects.filter(
                Q(bibliographicCitation__icontains=query) 
            )
            results = []
            for pl in object_list:
                if str(query).lower() in str(pl.bibliographicCitation).lower():
                    results = results + [pl.bibliographicCitation]

        # Get unique values
        results_unique = []
        for x in results:
            if x not in results_unique:
                results_unique.append(x)

        # Limite to 7 elements
        results_unique = results_unique[:7]

        data = json.dumps(results_unique)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

# ----------
