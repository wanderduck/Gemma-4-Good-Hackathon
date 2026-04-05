# Minnesota Benefits Programs, APIs, and Data Sources - Deep Dive

*Research compiled: 2026-04-05 for the Gemma 4 Good Hackathon - Plain Language Government Navigator*

---

## Table of Contents

1. [Minnesota State-Level Programs](#1-minnesota-state-level-programs)
2. [Application Portals and Screening Tools](#2-application-portals-and-screening-tools)
3. [Twin Cities Metro Counties Deep Dive](#3-twin-cities-metro-counties-deep-dive)
4. [Community Action Agencies](#4-community-action-agencies)
5. [Data Sources, APIs, and Open Data Portals](#5-data-sources-apis-and-open-data-portals)
6. [Minnesota Statutes and Policy Manuals](#6-minnesota-statutes-and-policy-manuals)
7. [Additional Resources and Tools](#7-additional-resources-and-tools)
8. [Architecture Implications for the Navigator](#8-architecture-implications-for-the-navigator)

---

## 1. Minnesota State-Level Programs

### Important Organizational Note (2024-2025 Restructuring)

On July 1, 2024, Minnesota created the **Department of Children, Youth, and Families (DCYF)** -- a new cabinet-level agency that absorbed child welfare, child care, child support, public benefits for low-income families, and homeless youth services from DHS and other agencies. Programs transitioned between July 2024 and July 2025. As of 2026:

- **DCYF** (dcyf.mn.gov) now administers: SNAP, MFIP, CCAP, Emergency Assistance, and related family programs
- **DHS** (mn.gov/dhs) retains: Medical Assistance, MinnesotaCare, disability services, aging services, Housing Support, behavioral health
- **MNsure** (mnsure.org) remains the health insurance marketplace
- **DEED** (mn.gov/deed) retains: Unemployment Insurance, Dislocated Worker Program, CareerForce
- **Commerce** (mn.gov/commerce) retains: Energy Assistance Program (EAP/LIHEAP)
- **Minnesota Housing** (mnhousing.gov): Housing finance programs

This restructuring means some web links and organizational references are in flux. The Navigator must handle both DHS and DCYF references.

---

### 1.1 Health Coverage Programs

#### Medical Assistance (MA) -- Minnesota's Medicaid
- **Administering Agency**: DHS (Health Care Eligibility and Access Division)
- **URL**: https://mn.gov/dhs/people-we-serve/adults/health-care/health-care-programs/programs-and-services/income-asset-limits.jsp
- **Eligibility**: Income-based. Single adult (19-64): ~$20,814/year or less. No monthly premium. Co-pays $1-$3 for some services.
- **Statute**: Minnesota Statutes Chapter 256B
- **Application**: Through MNsure or county/tribal office

#### MinnesotaCare
- **Administering Agency**: DHS
- **URL**: https://www.mnsure.org/financial-help/ma-mncare/
- **Eligibility**: Ages 19-64, income 138%-200% FPL ($31,300/individual, $64,300/family of 4 in 2026). Not eligible for MA or Medicare. No affordable employer coverage. Requires monthly premium.
- **Statute**: Minnesota Statutes Chapter 256L
- **Application**: Through MNsure only

#### MNsure (Health Insurance Marketplace)
- **URL**: https://www.mnsure.org/
- **What it covers**: Medical Assistance, MinnesotaCare, and marketplace plans with Advanced Premium Tax Credits (APTC)
- **Income Guidelines**: https://www.mnsure.org/financial-help/income-guidelines/index.jsp
- **PDF (2026)**: https://www.mnsure.org/assets/MNsure-2026-incomeguidelines-english_tcm34-702546.pdf
- **Access Method**: Web application only. No public API.

---

### 1.2 Cash Assistance Programs

#### Minnesota Family Investment Program (MFIP) -- Minnesota's TANF
- **Administering Agency**: DCYF (dcyf.mn.gov)
- **URL**: https://dcyf.mn.gov/programs-directory/minnesota-family-investment-program-mfip
- **Eligibility**: Families with children in poverty. Asset limit $10,000. Combined cash and food assistance.
- **Statute**: Minnesota Statutes Chapter 256J
- **Application**: MNbenefits.mn.gov or county office

#### General Assistance (GA)
- **Administering Agency**: DHS (via counties)
- **URL**: https://mn.gov/dhs/people-we-serve/adults/economic-assistance/income/programs-and-services/ga.jsp
- **Eligibility**: Monthly cash grants for vulnerable persons (15 eligibility categories based on disability/un-employability). Income and assets below program limits.
- **Statute**: Minnesota Statutes Chapter 256D
- **Who qualifies**: Single adults without children who meet at least one of 15 statutory categories (disability, age, domestic violence, etc.)

#### Minnesota Supplemental Aid (MSA)
- **Administering Agency**: DHS (via counties)
- **Eligibility**: Supplements SSI/Social Security for elderly, blind, or disabled individuals with income and assets within limits.
- **Statute**: Minnesota Statutes Chapter 256D

#### Diversionary Work Program (DWP)
- **Administering Agency**: DCYF
- **Eligibility**: Short-term (4 months) employment-focused alternative to MFIP for families who can work immediately.
- **Statute**: Minnesota Statutes 256J.95

---

### 1.3 Food Assistance

#### SNAP (Supplemental Nutrition Assistance Program)
- **Administering Agency**: DCYF
- **URL**: https://dcyf.mn.gov/snap
- **Eligibility**: Minnesota uses Broad-Based Categorical Eligibility (BBCE) with 200% FPL gross income limit. Benefits range $292/month (1 person) to $1,759 (8 people), ~$219 per additional member. Over 500,000 Minnesotans served.
- **Application**: MNbenefits.mn.gov

#### Minnesota Food Assistance Program (MFAP)
- **Administering Agency**: DCYF
- **URL**: https://dcyf.mn.gov/programs-directory/minnesota-food-assistance-program-mfap
- **Eligibility**: State-funded food assistance for lawfully present noncitizens who meet SNAP eligibility but are excluded from federal SNAP due to immigration status.

#### WIC (Women, Infants, and Children)
- **Administering Agency**: Minnesota Department of Health
- **URL**: https://www.health.state.mn.us/people/wic/index.html
- **Eligibility**: Income at or below 185% FPL. Must be pregnant, postpartum (up to 6 months), breastfeeding, or a child under 5. Auto-eligible if on SNAP, Medicaid, or MFIP.
- **Phone**: 1-800-942-4030

---

### 1.4 Emergency Assistance Programs

#### Emergency Assistance (EA)
- **Administering Agency**: DCYF (via counties)
- **URL**: https://dcyf.mn.gov/programs-directory/emergency-assistance
- **Eligibility**: Pregnant women or families with minor children facing housing crisis. One-time payment for rent/mortgage/utilities.
- **Application**: MNbenefits.mn.gov

#### Emergency General Assistance (EGA)
- **Administering Agency**: DHS (via counties)
- **Eligibility**: Income below 200% FPL. Cannot have received EGA in past 12 months. Cannot be on MFIP. Must have an emergency threatening physical health/safety. Basic needs: food, clothing, shelter, utilities.
- **Scope**: One-time only within 12 months.

---

### 1.5 Child Care

#### Child Care Assistance Program (CCAP)
- **Administering Agency**: DCYF (via counties)
- **URL**: https://dcyf.mn.gov/programs-directory/child-care-assistance-program
- **Policy Manual**: https://www.dhs.state.mn.us/main/idcplg?IdcService=GET_DYNAMIC_CONVERSION&RevisionSelectionMethod=LatestReleased&dDocName=CCAP_02
- **Eligibility**: Income at or below 47% SMI (67% if on MFIP/DWP). Exit threshold: 85% SMI. Income guidelines update Oct. 12, 2026.
- **Application**: MNbenefits.mn.gov

---

### 1.6 Housing Programs

#### Housing Support (formerly Group Residential Housing / GRH)
- **Administering Agency**: DHS
- **URL**: https://mn.gov/dhs/people-we-serve/adults/services/housing/programs-and-services/housing-support.jsp
- **Eligibility**: Age 65+ or disabling condition. Low income. Pays room and board.
- **Benefit Amounts**: $1,192/month (group settings), $1,242/month (community settings) as of July 1, 2025.
- **Application**: County/tribal office

#### Bridging Benefits
- **Administering Agency**: DHS
- **URL**: https://mn.gov/dhs/people-we-serve/adults/services/housing/programs-and-services/bridging-benefits.jsp
- **Purpose**: Short-term rental assistance while waiting for permanent housing subsidy.

#### Section 8 / Housing Choice Vouchers (Metro HRA)
- **Administering Agency**: Metropolitan Council Metro HRA
- **URL**: https://metrocouncil.org/Housing/Services/Metro-HRA-Rental-Assistance.aspx
- **Coverage**: Anoka, Carver, and suburban Hennepin and Ramsey counties. 7,200+ households served.
- **Programs**: Housing Choice Voucher (Section 8), Project Based Voucher (PBV), Family Affordable Housing Program (FAHP - 150+ single family homes).

#### Minnesota Housing Finance Agency (MHFA)
- **URL**: https://www.mnhousing.gov/
- **Programs**:
  - **Start Up** first-time homebuyer loans with low fixed rates (conventional, FHA, VA, USDA)
  - Downpayment/closing cost assistance up to $18,000
  - **First-Generation Homebuyer Loan**: Up to $35,000, ~1,500 borrowers, first-come first-served
  - Short-term rental/mortgage assistance (usually 3 months or less) for at-risk households
  - Rental assistance for people with serious mental illness
  - Requires homebuyer education course for first-time buyers

---

### 1.7 Energy Assistance

#### Energy Assistance Program (EAP) / LIHEAP
- **Administering Agency**: Minnesota Department of Commerce
- **URL**: https://mn.gov/commerce/energy/consumer-assistance/energy-assistance-program/guidelines.jsp
- **Eligibility**: Income at or below 50% State Median Income (SMI). Uses past 1 month of household income.
- **Benefits (FY2026)**: Heating: $200-$1,400. Crisis: up to $600.
- **Deadline**: Application deadline May 31, 2026. Season runs Oct 1 - May 31.
- **Administered locally by**: Community Action Agencies (CAP-HC, CAPRW, CAP Agency, etc.)

#### Weatherization Assistance Program
- Available year-round. Energy-saving services: caulking, weather-stripping, insulation, heating system tune-ups.
- Delivered by Community Action Agencies.

---

### 1.8 Employment and Workforce Programs

#### Unemployment Insurance
- **Administering Agency**: DEED (mn.gov/deed)
- **Application**: uimn.org (online filing)

#### Dislocated Worker Program
- **Administering Agency**: DEED via CareerForce
- **URL**: https://mn.gov/deed/programs-services/dislocated-worker/
- **CareerForce**: https://careerforce.mn.gov/dislocatedworker
- **Eligibility**: Age 18+, lost job through no fault of own (not quit/fired). Also: self-employed who lost income, veterans leaving active duty, National Guard members.
- **Services**: Career exploration, skills assessment, resume writing, interview prep, training.

#### CLIMB (Converting Layoffs into Minnesota Businesses)
- **URL**: https://careerforce.mn.gov/CLIMB
- **What it does**: Entrepreneurship training and consulting for dislocated workers. Business launch support through SBDCs.

#### SNAP Employment and Training (SNAP E&T)
- Available in Hennepin County and other areas. Job resources, support, and training for SNAP recipients.

#### CareerForce System
- **URL**: https://careerforce.mn.gov/
- Minnesota's unified workforce system. 16 local workforce boards. Multiple physical locations across Twin Cities metro.
- Services: career counseling, skills assessment, job search, training referrals.

---

## 2. Application Portals and Screening Tools

### 2.1 MNbenefits (Primary Application Portal)
- **URL**: https://mnbenefits.mn.gov/
- **FAQ**: https://mnbenefits.mn.gov/faq
- **What it does**: Online application for SNAP, MFIP, GA, MSA, Emergency Assistance, CCAP, Housing Support (GRH). Apply for multiple programs in one 20-minute application. Upload documents.
- **Replaced**: ApplyMN (being phased out county by county)
- **Languages**: Multiple (English primary)
- **API**: None public. Web-only.
- **Significance for Navigator**: This is where users end up after eligibility screening. The Navigator should link directly to MNbenefits.

### 2.2 Bridge to Benefits (Screening Tool)
- **URL**: https://bridgetobenefits.org/ScreeningTool
- **Operator**: Children's Defense Fund-Minnesota
- **What it does**: Free online pre-screening tool. 12 questions including household income, size, ages. Returns estimated eligibility for 12+ programs with estimated benefit amounts.
- **Programs screened**: Medical Assistance, MinnesotaCare, APTC, CCAP, Early Learning Scholarships, Energy Assistance, SNAP, School Meal Program, WIC, EITC, Working Family Credit.
- **Limitation**: Pre-screening only, not eligibility determination. Must still apply to each program.
- **API**: None. Web form only.
- **Significance for Navigator**: This is our closest existing competitor for MN. Our Navigator should exceed its coverage and provide conversational plain-language guidance.

### 2.3 Help Me Connect
- **URL**: https://helpmeconnect.web.health.state.mn.us/HelpMeConnect/
- **Operator**: Minnesota Department of Health
- **What it does**: Resource directory for pregnant/parenting families with children birth to age 8. Includes nonprofits, government, licensed providers.
- **Launched**: May 2021. 200,000+ visitors from all MN regions.
- **API**: None public. Web searchable directory.
- **Significance**: Good reference for early childhood services. Limited scope (under 8 only).

### 2.4 DB101 Minnesota (Disability Benefits 101)
- **URL**: https://mn.db101.org/
- **Operator**: Part of Disability Hub MN
- **What it does**: Interactive tools and information for people with disabilities. Covers SSI, SSDI, Section 8, Housing Support, MFIP, SNAP, GA, MA. Includes benefit estimators showing how income affects benefits.
- **Unique value**: Shows how WORKING affects benefits -- key for disability population.
- **Expert Chat**: Connects to real Disability Hub MN experts.
- **API**: None. Web tools only.

### 2.5 findhelp.org (formerly Aunt Bertha)
- **URL**: https://www.findhelp.org/find-social-services/minnesota
- **What it does**: Nationwide social services directory. Search by zip code.
- **Find Help Minnesota**: Statewide behavioral health program locator with real-time inpatient bed capacity tracking. Launched April 2025.
- **API**: findhelp has commercial APIs for healthcare system integration. Not free/public.
- **Data Standard**: Uses its own format but aligns with Open Referral concepts.

### 2.6 Combined Application Form (CAF) / DHS-5223
- **URL**: https://www.dhs.state.mn.us/main/groups/county_access/documents/pub/dhs16_166607.pdf
- **What it does**: Paper form covering MFIP, DWP, SNAP, MSA, GA, GRH on one application.
- **Significance**: The form's structure reveals what data points are needed for eligibility -- useful for designing the Navigator's question flow.

---

## 3. Twin Cities Metro Counties Deep Dive

### 3.1 Ramsey County (St. Paul)

**County Seat**: St. Paul
**Population**: ~557,000
**Main Social Services URL**: https://www.ramseycountymn.gov/residents/assistance-support/
**Phone**: 651-266-3800 (24/7 EZ Info line -- English, Spanish, Hmong, Somali, Karen)

#### Programs Administered

| Program | URL | Notes |
|---|---|---|
| Financial Assistance (SNAP, MFIP, GA, MSA, EA, CCAP) | https://www.ramseycountymn.gov/residents/assistance-support/assistance/financial-assistance | Apply via MNbenefits.mn.gov |
| Emergency Assistance | https://www.ramseycountymn.gov/residents/assistance-support/assistance/financial-assistance/emergency-assistance | Short-term for rent, housing, utilities |
| Child Care Assistance | https://www.ramseycountymn.gov/residents/assistance-support/assistance/financial-assistance/child-care-assistance | Via MNbenefits |
| Dislocated Worker Program | https://www.ramseycountymn.gov/residents/assistance-support/employment-assistance/job-seeker-programs/dislocated-worker-program | County-run program with interest form and dedicated application |
| Dislocated Worker Application | https://www.ramseycountymn.gov/residents/assistance-support/employment-assistance/job-seeker-programs/dislocated-worker-program/dislocated-worker-program-application | 5 business day response |
| Rental Assistance | https://www.ramseycountymn.gov/residents/assistance-support/assistance/rental-assistance | Including Neighborhood House funds |
| Social Services Directory | https://www.ramseycountymn.gov/your-government/departments/health-wellness/social-services/directory | Full directory of all services |

#### County-Specific Highlights
- **Dislocated Worker Program** is county-operated (not just state-level referral). Has its own online interest form and application.
- **24/7 EZ Info Line** (651-266-3800) in 5 languages is a notable accessibility feature.
- **Open Data Portal**: https://opendata.ramseycountymn.gov/ -- 130+ datasets, charts, maps. Public safety, administration, demographics, health, transportation, budget data.
- **GIS Portal**: https://data-ramseygis.opendata.arcgis.com/ -- ArcGIS-based. API links for GeoServices, WMS, WFS. Download in CSV, KML, GeoJSON, GeoTIFF, PNG.

---

### 3.2 Hennepin County (Minneapolis)

**County Seat**: Minneapolis
**Population**: ~1.28 million (largest MN county)
**Main Human Services URL**: https://www.hennepin.us/en/residents/human-services
**Human Services Budget (2026)**: $846.1 million operating budget, 3,718 FTEs

#### Programs Administered

| Program | URL | Notes |
|---|---|---|
| Cash Assistance (MFIP, GA, MSA, DWP) | https://www.hennepin.us/en/residents/human-services/cash-assistance | ~6,900 MFIP families, ~19,000 individuals |
| SNAP | Via MNbenefits | ~110,000 active recipients |
| Emergency Programs | https://www.hennepin.us/en/residents/human-services/emergency-assistance | EA, EGA, special diet food support, foreclosure prevention |
| Child Care Assistance | https://www.hennepin.us/en/residents/human-services/child-care-assistance | |
| Workforce Development | https://www.hennepin.us/residents/human-services/workforce-development | |
| Employment Services (Job Seekers) | https://www.hennepin.us/employmentservices | |
| Hennepin Pathways | https://www.hennepin.us/pathways-program | County employment program in office admin, human services, building ops |

#### Caseload Numbers (2026 Budget)
- **SNAP**: ~110,000 active recipients
- **MFIP**: ~6,900 families (~19,000 individuals)
- **WIC**: ~13,000 individuals

#### Workforce Programs
- **Hennepin-Carver Workforce Development Board**: https://hennepincarverworkforce.org/ -- Oversees CareerForce locations in suburban Hennepin and Carver County.
- **SNAP E&T**: Job resources and training for SNAP recipients.
- **WIOA Young Adult Program**: Ages 14-24 experiencing homelessness, justice involvement, poverty.
- **Dislocated Worker Program**: For workers transitioning from layoffs.
- **Hennepin Pathways**: County-run employment program placing graduates in county jobs.

#### Data Resources
- **Human Services Data and Reports**: https://www.hennepin.us/en/your-government/research-data/human-services-public-health-volume-data
- **GIS Open Data**: https://gis-hennepin.opendata.arcgis.com/ -- ArcGIS Hub. Free spatial data, no license needed. CSV, KML, GeoJSON, GeoTIFF, PNG. API: GeoServices, WMS, WFS.
- **Research and Data**: https://www.hennepin.us/your-government/open-government/open-government

---

### 3.3 Dakota County

**County Seat**: Hastings
**Population**: ~444,000
**Main Public Assistance URL**: https://www.co.dakota.mn.us/HealthFamily/PublicAssistance
**Phone**: 651-554-5611 (Employment & Economic Assistance)
**Hours**: Mon-Fri 8am-4:30pm (walk-ins until 4pm)

#### Programs Administered

| Program | URL | Notes |
|---|---|---|
| Food Assistance (SNAP) | https://www.co.dakota.mn.us/HealthFamily/PublicAssistance/Food/Pages/default.aspx | |
| Cash/Emergency Assistance | Via MNbenefits | MFIP, GA, MSA, EGA, EA |
| Child Care Assistance | Via MNbenefits | |
| Emergency Assistance | https://www.co.dakota.mn.us/HealthFamily/PublicAssistance/Emergency/Pages/default.aspx | One-time payment for eviction/utility shutoff |
| Aging & Disability Services | https://www.co.dakota.mn.us/HealthFamily/Disabilities | MN Choices Assessment, DD services, PCA, waiver services |
| Community Living Services | Phone: 651-554-6336 | Consumer Support, Family Support Grants, housing with services |

#### Service Locations
- **Western Service Center**: 14955 Galaxie Ave., Apple Valley
- **Northern Service Center**: 1 Mendota Road W., Suite 100, West St. Paul

#### Data Resources
- **GIS Data**: https://www.co.dakota.mn.us/HomeProperty/MappingServices/GISData/Pages/default.aspx -- Free, no restrictions. Available on Minnesota Geospatial Commons.
- **Community Resource Guide (PDF)**: https://www.co.dakota.mn.us/HealthFamily/HealthServices/MoreLowCostServices/Documents/CommunityResourceGuide.pdf

---

### 3.4 Scott County

**County Seat**: Shakopee
**Population**: ~153,000
**Main Social Services URL**: https://www.scottcountymn.gov/193/Social-Services
**Income Maintenance**: https://www.scottcountymn.gov/296/Income-Maintenance-Financial-Assistance

#### Programs Administered

| Program | URL | Notes |
|---|---|---|
| Income Maintenance / Financial Assistance | https://www.scottcountymn.gov/296/Income-Maintenance-Financial-Assistance | SNAP, MFIP, GA, MSA, EGA, CCAP, MA, RCA |
| Disability Services | https://www.scottcountymn.gov/2367/Aging-and-Disability-Services-Programs | Children and adults with disabilities |
| Adult Mental Health | Part of Social Services | Case management, community support for SPMI |
| Senior Services | https://www.scottcountymn.gov/1237/Senior-Services | |
| Community Connections Guide | https://www.scottcountymn.gov/DocumentCenter/View/19201/Community-Connections-Guide-pdf | Comprehensive local resource guide |

#### Key Details
- Administers all mandated public assistance programs: cash, SNAP, child care, health care.
- Programs include EGA, GA, MFIP, MSA, Refugee Cash Assistance (RCA).
- Home and Community Care Programs help seniors and persons with disabilities live independently.

---

### 3.5 Carver County

**County Seat**: Chaska
**Population**: ~107,000
**Main HHS URL**: https://www.carvercountymn.gov/departments/health-human-services
**Phone**: (952) 361-1600
**Address**: 602 E 4th St, Chaska

#### Programs Administered

| Program | Notes |
|---|---|
| Financial Assistance | SNAP, MFIP, GA, MSA, EGA |
| Food Support | SNAP benefits |
| Child Care Assistance | CCAP |
| Health Care Coverage | MA, MinnesotaCare via MNsure |
| Long-Term Care | Waiver services, PCA, disability services |
| Emergency Assistance | EA for families, EGA for individuals |

#### Data Resources
- **GIS Portal**: https://data-carver.opendata.arcgis.com/ -- ArcGIS open data. Parcels, boundaries, etc.
- **Family Resource Guide (PDF)**: https://www.carvercda.org/media/userfiles/subsite_275/files/housing/Family-Resource-Guide.pdf

---

## 4. Community Action Agencies

### 4.1 Community Action Partnership of Ramsey & Washington Counties (CAPRW)
- **URL**: https://www.caprw.org/
- **Address**: 450 Syndicate St N, Saint Paul, MN 55104
- **Phone**: (651) 645-6445
- **Serves**: Ramsey and Washington counties
- **Founded**: 1964 (War on Poverty)

#### Programs
| Program | Description |
|---|---|
| Energy Assistance (EAP) | Bill payment assistance, crisis intervention, furnace/boiler repair, outreach, advocacy, utility rights info |
| Energy Conservation | Weatherization and energy efficiency services |
| Head Start & Early Head Start | Income-based early education |
| SNAP Screening & Application Assistance | Help applying for food assistance |
| Car Loan Program | Vehicle financing for low-income workers |
| Matched Savings Program | Financial empowerment |
| Financial Literacy Classes | Budgeting, money management |
| Employment Assistance & Job Training | Workforce development |
| VITA Tax Clinic | Free tax preparation |
| FAIR Checking, Savings & Credit Builder | Financial products for unbanked/underbanked |
| Voter Education & Registration | Civic engagement |
| Section 8 Housing Applications | Housing Choice Vouchers (when waitlist opens) |

---

### 4.2 Community Action Partnership of Hennepin County (CAP-HC)
- **URL**: https://caphennepin.org/
- **Formerly**: Community Action Partnership of Suburban Hennepin (CAPSH)
- **Serves**: Hennepin County (primarily suburban areas)

#### Programs
| Program | Description |
|---|---|
| Energy Assistance | Gas and electric bill payment help |
| Water Assistance | Water bill payment help |
| Rental Assistance | One-time payment for rent or security deposit |
| Vehicle Repair Program | Help paying for vehicle repairs for work transportation |
| Employment Readiness | Help finding living-wage jobs |
| Financial Wellness | Free workshops, counseling, budgeting, money management |
| Homebuyer Services | Homebuyer workshops and free counseling |
| Tax Assistance | Free and low-cost tax filing |

---

### 4.3 Community Action Partnership of Scott, Carver, and Dakota Counties (CAP Agency)
- **URL**: https://capagency.org/
- **Serves**: Scott, Carver, and Dakota counties
- **How We Help**: https://capagency.org/how-we-help/
- **Annual Impact**: 50,000 individuals served
- **History**: Nearly 60 years of operation

#### Offices
| Location | Address | Phone | Hours |
|---|---|---|---|
| Dakota County | 2496 145th St W, Rosemount, MN 55068 | 651-322-3500 | M-F 8am-4:30pm |
| Scott County | 738 1st Ave E, Shakopee, MN 55379 | (listed on site) | M-F 8am-4:30pm |
| Carver County | 110 W 2nd St, Chaska, MN 55318 | 952-496-2125 | M-F 8am-4:30pm |

#### Programs (20+ established programs)
| Program | Description |
|---|---|
| Energy Assistance | Bill payment, crisis intervention |
| Emergency Repair Replacement (ERR) | Furnace/heating system repair or replacement for owner-occupied homes |
| Head Start | Income-based early education for children 3-5 |
| Early Head Start | Children birth to 3, plus expecting mothers. Phone: 651-322-3500 option 2 |
| Chore Program | Senior yard maintenance, homemaker services, assisted transportation, home modification |
| Housing Services | Various housing stability programs |
| Employment Programs | Workforce development and job placement |

---

## 5. Data Sources, APIs, and Open Data Portals

### 5.1 State-Level Data Sources

#### Minnesota Open Data Portal
- **URL**: https://www.state.mn.us/opendata/data.html
- **What it contains**: State-level open datasets across departments
- **Access**: Web browsable. Some datasets downloadable.
- **Platform**: Unknown (not confirmed CKAN/Socrata -- needs direct investigation)

#### Minnesota Geospatial Commons
- **URL**: https://gisdata.mn.gov/
- **What it contains**: GIS/geospatial data from all state agencies and counties. Maps, services, applications.
- **Access**: Free downloads in multiple formats. APIs for web map services.
- **Significance**: All 7 metro counties have adopted free/open geospatial data policies as of 2015.

#### MetroGIS
- **URL**: https://metrogis.org/projects/free-plus-open-data/
- **What it contains**: Coordinated free and open geospatial data for the Twin Cities metro region.

#### Minnesota IT Services / MnGeo
- **URL**: https://mn.gov/mnit/about-mnit/mngeo/gis-data-maps.jsp
- **What it does**: Coordination, guidance, and leadership for state GIS use.

#### Data.gov - State of Minnesota
- **URL**: https://catalog.data.gov/organization/state-mn-us
- **What it contains**: Federal catalog of Minnesota state datasets.

---

### 5.2 County-Level Open Data

| County | Portal URL | Platform | Content |
|---|---|---|---|
| Ramsey | https://opendata.ramseycountymn.gov/ | Tyler Technologies (Socrata-like) | 130+ datasets: public safety, admin, demographics, health, transportation, budgets |
| Ramsey GIS | https://data-ramseygis.opendata.arcgis.com/ | ArcGIS Hub | Geospatial data with REST APIs |
| Hennepin GIS | https://gis-hennepin.opendata.arcgis.com/ | ArcGIS Hub | Spatial data, free, no license |
| Hennepin HS Data | https://www.hennepin.us/en/your-government/research-data/human-services-public-health-volume-data | Custom | Human services volume data and reports |
| Dakota GIS | https://www.co.dakota.mn.us/HomeProperty/MappingServices/GISData/ | MN Geospatial Commons | Free, no restrictions |
| Carver GIS | https://data-carver.opendata.arcgis.com/ | ArcGIS Hub | Parcels, boundaries |
| Minneapolis | https://opendata.minneapolismn.gov/ | ArcGIS Hub | CC BY-SA 4.0 license. Full API. |

**Note**: Scott County does not appear to have a dedicated open data portal. GIS data is available through the Minnesota Geospatial Commons.

---

### 5.3 211 United Way Data

#### Greater Twin Cities United Way 211
- **URL**: https://www.gtcuw.org/get-assistance/211-resource-helpline/
- **What it does**: 40,000+ programs and services in database. Largest call center in Minnesota.
- **How to access**: Dial 2-1-1, text your zip code to 898-211, or go online.

#### 211 National Data Platform API
- **Developer Portal**: https://register.211.org/ (also https://api-devportal-dev.211.technology/)
- **APIs Available**:
  - **Search API**: Keyword/guided search, filters, returns service-at-location resource data
  - **Export API**: Bulk data export of organizations for import into external systems
  - **Resources API**: Query repository for contacts, services, locations, organizations
- **Data Standard**: Aligns with Open Referral HSDS
- **Access**: Register for developer account, subscribe to Trial product for development access
- **License**: Proprietary (locally curated). Access is registration-gated.
- **Competition Compliance**: UNCERTAIN -- needs investigation of terms of use.

---

### 5.4 Open Data Standards

#### Open Referral / HSDS (Human Services Data Specification)
- **URL**: https://docs.openreferral.org/
- **Spec Version**: 3.0.1 (latest)
- **What it is**: Machine-readable exchange format for health, human, and social services data.
- **GitHub**: https://github.com/openreferral/specification
- **License**: CC BY-SA
- **Significance**: If we structure our Navigator's services database in HSDS format, it becomes interoperable with 211, findhelp, and other systems.

#### Open Eligibility Taxonomy
- **GitHub**: https://github.com/auntbertha/openeligibility (also https://github.com/openreferral/openeligibility)
- **What it is**: Standardized taxonomy of Human Services (housing, food, counseling) and Human Situations (veterans, disability, seniors).
- **Formats**: XML, CSV, JSON, YAML
- **License**: CC BY-SA 3.0
- **Significance**: Use as classification backbone for matching users to services.

---

### 5.5 Ramsey County Open Data Deep Dive

The Ramsey County Open Data Portal at https://opendata.ramseycountymn.gov/ is the most feature-rich county portal of our 5 target counties. Key features:

- **Stories**: Interactive data stories including the Dislocated Worker Program page at https://opendata.ramseycountymn.gov/stories/s/Dislocated-Worker-Program/48jf-m4q6/
- **Finance Data**: Budget visualization, revenue, expenditure data
- **Datasets**: 130+ datasets with download and API access
- **ArcGIS REST API**: https://maps.co.ramsey.mn.us/arcgis/rest/services/OpenData/OpenData/FeatureServer
- **Download Formats**: CSV, KML, Zip, GeoJSON, GeoTIFF, PNG

---

## 6. Minnesota Statutes and Policy Manuals

### 6.1 Minnesota Revisor of Statutes
- **URL**: https://www.revisor.mn.gov/statutes/
- **Key Chapters**:
  - **Ch. 119B**: Child care assistance
  - **Ch. 256**: Human services generally; health care benefits
  - **Ch. 256B**: Medical Assistance (Medicaid)
  - **Ch. 256D**: GA and MSA programs
  - **Ch. 256J**: MFIP (Minnesota's TANF)
  - **Ch. 256L**: MinnesotaCare
  - **Ch. 268**: Unemployment insurance
- **Machine-Readable Access**: Bill status available as XML (append &format=xml to search URLs). Full statute text is HTML only.
- **Alternative**: LegiScan (legiscan.com/MN/datasets) offers MN legislative archives in JSON, XML, CSV.

### 6.2 DHS Combined Manual (Economic Assistance Policy)
- **URL**: https://www.dhs.state.mn.us/main/idcplg?IdcService=GET_DYNAMIC_CONVERSION&RevisionSelectionMethod=LatestReleased&dDocName=ID_016956
- **What it covers**: Complete policy manual for financial workers determining eligibility for MFIP, DWP, SNAP, GA, GRH/Housing Support, MSA, RCA, and Emergency programs.
- **Sections include**: Gross income limits, assistance standards, benefit calculation, application processing.
- **Access**: Web-based HTML pages. No API or bulk download. Could be scraped for RAG knowledge base.
- **Significance**: THE authoritative source for eligibility rules for cash/food programs. Essential for building accurate eligibility logic.

### 6.3 DHS Eligibility Policy Manual (Health Care)
- **URL**: https://hcopub.dhs.state.mn.us/epm/home.htm
- **What it covers**: Official eligibility policies for Medical Assistance and MinnesotaCare.
- **Access**: Web-based HTML pages. No API or bulk download.
- **Updates**: Policy changes announced via email subscription (since June 2023).

### 6.4 CCAP Policy Manual
- **URL**: https://www.dhs.state.mn.us/main/idcplg?IdcService=GET_DYNAMIC_CONVERSION&RevisionSelectionMethod=LatestReleased&dDocName=CCAP_02
- **What it covers**: Complete child care assistance eligibility and administration policies.

---

## 7. Additional Resources and Tools

### 7.1 LawHelp Minnesota
- **URL**: https://www.lawhelpmn.org/
- **What it does**: Free legal information and self-help resources. Fact sheets on EGA, GA, SNAP, housing rights.
- **Significance**: Plain-language legal explanations of benefits programs. Good RAG source.

### 7.2 Disability Hub MN
- **URL**: https://disabilityhubmn.org/
- **What it does**: Central resource for Minnesotans with disabilities. Connects to DB101, Chat with Expert, benefits planning.

### 7.3 mn.gov/adresources
- **URL**: https://mn.gov/adresources/search/
- **What it does**: Aging and Disability Resource search. Searchable directory of providers by program type and location.

### 7.4 Minnesota House Research Department Publications
- **URL**: Various at house.mn.gov/hrd/pubs/
- **Key Publications**:
  - CCAP overview: https://www.house.mn.gov/hrd/pubs/pap_ccap.pdf
  - MinnesotaCare: https://www.house.mn.gov/hrd/pubs/mncare.pdf
  - EGA basics: https://www.house.mn.gov/hrd/pubs/ss/ssegaea.pdf
  - MHFA programs: https://www.house.mn.gov/hrd/pubs/mhfaprog.pdf
- **Significance**: These are excellent plain-language summaries of program rules. Good for RAG.

### 7.5 Hennepin-Carver Workforce Development Board
- **URL**: https://hennepincarverworkforce.org/
- **Program Descriptions**: https://hennepincarverworkforce.org/program-descriptions/
- **Programs**: SNAP E&T, WIOA Young Adult, Dislocated Worker, Adult Employment

---

## 8. Architecture Implications for the Navigator

### 8.1 Data Collection Strategy

Based on this research, the Navigator's knowledge base should be built from these tiers:

**Tier 1 -- Structured/API Data (highest quality)**
- NYC Benefits Screening API (for federal program eligibility logic -- reusable even if NYC-specific)
- SAM.gov Assistance Listings API (federal program directory)
- 211 National Data Platform APIs (local services directory, if access permitted)
- HUD income limits API (housing eligibility)
- CMS Marketplace API (health coverage)

**Tier 2 -- Scrapable Web Content (medium effort)**
- DHS Combined Manual (cash/food program eligibility rules)
- DHS Eligibility Policy Manual (health care eligibility rules)
- CCAP Policy Manual (child care eligibility)
- MN Revisor statutes chapters 119B, 256, 256B, 256D, 256J, 256L, 268
- Minnesota House Research Department program summaries
- Bridge to Benefits screening logic (reverse-engineer question flow)
- County social services pages (Ramsey, Hennepin, Dakota, Scott, Carver)
- Community Action Agency program pages

**Tier 3 -- PDF/Document Sources (highest effort)**
- MNsure income guidelines PDF
- CAF form (DHS-5223) for question flow design
- CCAP copayment schedules (DHS-6413N)
- Energy Assistance income guidelines
- Scott County Community Connections Guide
- Dakota County Community Resource Guide
- Carver County Family Resource Guide
- Mass Layoff Handbook / Small Layoff Handbook (DEED)

### 8.2 County-Specific Differentiation Matrix

| Feature | Ramsey | Hennepin | Dakota | Scott | Carver |
|---|---|---|---|---|---|
| Open Data Portal | Yes (130+ datasets) | GIS + HS data | GIS via MN Geospatial | No dedicated portal | GIS via ArcGIS |
| County-Run Dislocated Worker | Yes (own app) | Via Hennepin-Carver WDB | Via CareerForce | Via CareerForce | Via Hennepin-Carver WDB |
| CAP Agency | CAPRW | CAP-HC | CAP Agency (SCD) | CAP Agency (SCD) | CAP Agency (SCD) |
| Multilingual Phone Line | Yes (5 languages, 24/7) | Yes | Standard hours | Standard hours | Standard hours |
| Special Programs | Dislocated Worker interest form | Hennepin Pathways, SNAP E&T | Aging/Disability strong | Mental Health case mgmt | Small county, fewer extras |
| HRA/Section 8 | Metro HRA (suburban) | Metro HRA + Minneapolis PHA | Metro HRA | Metro HRA | Metro HRA |
| Application Portal | MNbenefits | MNbenefits | MNbenefits | MNbenefits | MNbenefits |

### 8.3 Key Insight: What Makes Our Navigator Different

Existing tools in Minnesota:
1. **Bridge to Benefits** -- Screens for ~12 programs but is a simple form, not conversational. No county-specific info.
2. **MNbenefits** -- Application portal, not a screening/navigation tool.
3. **Help Me Connect** -- Families with children under 8 only.
4. **DB101** -- Disability-focused only.
5. **211** -- Phone/text referral, not AI-powered plain-language.
6. **findhelp.org** -- Directory search, not conversational eligibility guidance.

**Our Navigator's unique value**:
- Conversational plain-language interface (powered by Gemma 4)
- Covers ALL program types (not just health, not just disability, not just families)
- County-specific guidance for the 5 target counties
- Knows about Community Action Agencies and their specific programs
- Explains eligibility in plain language, not bureaucratic jargon
- Guides users to the RIGHT application portal (MNbenefits, MNsure, CareerForce, CAP, etc.)
- Handles the DHS-to-DCYF transition confusion
- Multilingual potential (Hmong, Somali, Spanish, Karen -- key Twin Cities populations)

---

## Sources

### State Agencies
- [MN DHS Eligibility Policy Manual](https://hcopub.dhs.state.mn.us/)
- [MN DHS Combined Manual](https://www.dhs.state.mn.us/main/idcplg?IdcService=GET_DYNAMIC_CONVERSION&RevisionSelectionMethod=LatestReleased&dDocName=ID_016956)
- [MN DHS Income and Asset Limits](https://mn.gov/dhs/people-we-serve/adults/health-care/health-care-programs/programs-and-services/income-asset-limits.jsp)
- [MN DHS Data Requests](https://mn.gov/dhs/general-public/about-dhs/data-requests/index.jsp)
- [MN DCYF](https://dcyf.mn.gov/)
- [MN DCYF - Apply for Benefits](https://dcyf.mn.gov/apply-benefits)
- [MNbenefits](https://mnbenefits.mn.gov/)
- [MNsure](https://www.mnsure.org/)
- [MNsure Income Guidelines 2025-26](https://www.mnsure.org/financial-help/income-guidelines/index.jsp)
- [Bridge to Benefits](https://bridgetobenefits.org/ScreeningTool)
- [Help Me Connect](https://helpmeconnect.web.health.state.mn.us/HelpMeConnect/)
- [DB101 Minnesota](https://mn.db101.org/)
- [MN DEED Dislocated Worker](https://mn.gov/deed/programs-services/dislocated-worker/)
- [CareerForce](https://careerforce.mn.gov/)
- [MN Energy Assistance](https://mn.gov/commerce/energy/consumer-assistance/energy-assistance-program/guidelines.jsp)
- [Minnesota Housing](https://www.mnhousing.gov/)
- [MN Revisor of Statutes](https://www.revisor.mn.gov/statutes/)
- [MN Open Data](https://www.state.mn.us/opendata/data.html)
- [MN Geospatial Commons](https://gisdata.mn.gov/)
- [MN WIC Program](https://www.health.state.mn.us/people/wic/index.html)

### County Resources
- [Ramsey County Financial Assistance](https://www.ramseycountymn.gov/residents/assistance-support/assistance/financial-assistance)
- [Ramsey County Dislocated Worker](https://www.ramseycountymn.gov/residents/assistance-support/employment-assistance/job-seeker-programs/dislocated-worker-program)
- [Ramsey County Open Data](https://opendata.ramseycountymn.gov/)
- [Hennepin County Human Services](https://www.hennepin.us/en/residents/human-services)
- [Hennepin County Emergency Programs](https://www.hennepin.us/en/residents/human-services/emergency-assistance)
- [Hennepin County HS Data](https://www.hennepin.us/en/your-government/research-data/human-services-public-health-volume-data)
- [Hennepin GIS Open Data](https://gis-hennepin.opendata.arcgis.com/)
- [Dakota County Public Assistance](https://www.co.dakota.mn.us/HealthFamily/PublicAssistance)
- [Dakota County GIS](https://www.co.dakota.mn.us/HomeProperty/MappingServices/GISData/Pages/default.aspx)
- [Scott County Social Services](https://www.scottcountymn.gov/193/Social-Services)
- [Scott County Income Maintenance](https://www.scottcountymn.gov/296/Income-Maintenance-Financial-Assistance)
- [Carver County HHS](https://www.carvercountymn.gov/departments/health-human-services)
- [Carver County GIS](https://data-carver.opendata.arcgis.com/)
- [Metro HRA](https://metrocouncil.org/Housing/Services/Metro-HRA-Rental-Assistance.aspx)
- [Minneapolis Open Data](https://opendata.minneapolismn.gov/)

### Community Action Agencies
- [CAPRW (Ramsey & Washington)](https://www.caprw.org/)
- [CAP-HC (Hennepin)](https://caphennepin.org/)
- [CAP Agency (Scott, Carver, Dakota)](https://capagency.org/)
- [Hennepin-Carver Workforce Development](https://hennepincarverworkforce.org/)

### Data Standards and APIs
- [211 Developer Portal](https://register.211.org/)
- [Open Referral HSDS](https://docs.openreferral.org/)
- [Open Eligibility Taxonomy](https://github.com/auntbertha/openeligibility)
- [findhelp.org Minnesota](https://www.findhelp.org/find-social-services/minnesota)
- [LegiScan MN Archives](https://legiscan.com/MN/datasets)
- [Data.gov - State of Minnesota](https://catalog.data.gov/organization/state-mn-us)
- [MetroGIS](https://metrogis.org/projects/free-plus-open-data/)

### Income/Eligibility References
- [MinnesotaCare Income Limits 2026](https://learn.navitize.com/blog/minnesotacare-income-limits-2026)
- [MN Medicaid Income Limits](https://checkmedicaid.com/minnesota-medicaid-income-limits/)
- [MN SNAP Eligibility](https://snapeligibilitycalculator.com/snap-benefits-by-state/minnesota/)
- [LIHEAP Clearinghouse - Minnesota](https://liheapch.acf.gov/profiles/Minn.htm)
- [MN House Research - CCAP](https://www.house.mn.gov/hrd/pubs/pap_ccap.pdf)
- [MN House Research - MinnesotaCare](https://www.house.mn.gov/hrd/pubs/mncare.pdf)
- [MN House Research - EGA](https://www.house.mn.gov/hrd/pubs/ss/ssegaea.pdf)
- [MN House Research - MHFA Programs](https://www.house.mn.gov/hrd/pubs/mhfaprog.pdf)
- [LawHelp Minnesota - EGA](https://www.lawhelpmn.org/self-help-library/fact-sheet/emergency-general-assistance-ega)
