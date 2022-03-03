
### Project Assessment

  

To assess your project work, you should be able to answer the following questions:

  

 ### 1. For classifying product names to categories:

  
  

+  **What precision (P@1) were you able to achieve?**

+ The result of my best attempt with data pruned by `--min_products 200`

  

N 10000

P@1 0.887

R@1 0.887

  
  

-  **What fastText parameters did you use?**

+ In my early attempts after manual experiments I used an approach similar to grid search with the following parameters

` dim=(10, 20, 50, 100) lr=(0.1, 0.15, 0.3) wordNgrams=(1 2 3) epoch=(25, 50, 100)`

  

but then I used fasttext **autotune** feature to get the best model.

  
  

-  **How did you transform the product names?**

1. Lowercase() and strip() text

2. New line chars removed

3. Punctuation removed

4. Accented chars normalized

5. Stemming with SnowballStemmer

  
  

-  **How did you prune infrequent category labels, and how did that affect your precision?**

+ I took advantage of Pandas to remove infrequent labels.

+ without pruning infrequent category labels the best `P@1` I could get was **0.608** .

+ with `--min_products 50` I got : **0.728**

+ with `--min_products 100` I got : **0.812**

+ with `--min_products 200` I got : **0.887**

  

- ** How did you prune the category tree, and how did that affect your precision?**

+ I just added a new switch called `--cat_granularity_level` which basically recieves the number of backward steps from the leaf depth to select the right leaf ancestor and use it as a category label. here is the detail of my experiments on pruning at different levels

+ --min_products 100 --cat_granularity_level 1

+ 215 infrequent labels eliminated from dataset.

+  `N 10000 P@1 0.784 R@1 0.784`

+ --min_products 200 --cat_granularity_level 1

+ 274 infrequent labels eliminated from dataset.

+  `N 10000 P@1 0.817 R@1 0.817`

+ --cat_granularity_level 2

+  `N 9997 P@1 0.783 R@1 0.783`

+ --min_products 200 --cat_granularity_level 2

+  `N 10000 P@1 0.798 R@1 0.798`

  

+  **For deriving synonyms from content:**

 ### 2. For deriving synonyms from content:

+  **What 20 tokens did you use for evaluation?**


| product types | brands | models | attributes |
| :------------: | :------------: | :------------: | :------------: |
|headphones| sony | thinkpad | 128gb |
| laptops | apple | 4s | 1080p |
| printers | samsung | wii | wireless |
| readers | verizon | kindle | 4g |
| games | hp | pavilion | black |
  

+  **What fastText parameters did you use?**

+  `-minCount` and `-maxn`

  

+  **How did you transform the product names?**

+ Lowercase() and strip() text

+ New line chars removed

+ Punctuation removed

+ Accented chars normalized

  

+  **What threshold score did you use?**

+ 10, 20, 50 ,90

  

+  **What synonyms did you obtain for those tokens?**

  

+ headphones

	+ earbud 0.920056

		ear 0.881606

		bud 0.795909

		meelectronics 0.784429

		hesh 0.77814

		koss 0.777878

		canceling 0.777284

		isolating 0.772126

		akg 0.767492

		adidas 0.761716
		
		------------

+ laptops

	+ notebooks 0.857617

	pros 0.819543

	atg 0.814092

	netbooks 0.809488

	lenmar 0.79264

	ibm 0.789612

	polymer 0.787315

	powerbook 0.786575

	lithium 0.752353

	lifebook 0.747708

------------

+ printers

	+ toner 0.936915

	yield 0.933268

	ecotoneplus 0.930622

	cyan 0.907768

	remanufactured 0.907041

	nextlife 0.903402

	ortofon 0.901176

	officejet 0.884476

	vivera 0.881311

	cartridges 0.879617

------------

+ readers

	+ verso 0.897473

	nookcolor 0.887271

	barnes 0.869144

	kobo 0.863982

	nook 0.859922

	kindle 0.857236

	noble 0.85079

	amazon 0.840198

	jivo 0.829762

	timbuk2 0.820474

------------

+ games

	+ trademark 0.878467

		hardwood 0.831853

		cue 0.774857

		miller 0.763326

		billiard 0.761432

		dice 0.751082

		pool 0.746691

		wildlife 0.74248

		hoyle 0.738132

		global 0.737897

  ------------

+ sony

	+ dsc 0.632009

		w120 0.630094

		walkman 0.603656

		bravia 0.596276

		cyber 0.591972

		w 0.590219

		vaio 0.586115

		alpha 0.574077

		a330 0.5737

		w530 0.571381

  ------------

+ apple

	+ ipod 0.829925

		iphone 0.750718

		ipadTM 0.744828

		ipodTM 0.744528

		ipad 0.743578

		iskin 0.708331

		generation 0.699263

		isound 0.693946

		hurley 0.690947

		kickstand 0.683142

  ------------

+ samsung

	+ lg 0.762938

		google 0.640684

		sph 0.638167

		proof 0.63569

		lte 0.63308

		sch 0.622691

		net10 0.608619

		shine 0.607521

		huawei 0.601229

		fascinate 0.590254

  ------------

+ verizon

	+ sprint 0.908166

		hotspot 0.893791

		4g 0.87204

		huawei 0.870352

		pantech 0.858358

		gophone 0.854716

		net10 0.853408

		lte 0.851983

		8530 0.842245

		atrix 0.828608

  ------------

+ hp

	+ pavilion 0.812423

		920 0.795401

		hpe 0.784045

		1204 0.773967

		p7 0.773433

		h8 0.772444

		hewlett 0.768656

		s5 0.767785

		sempronTM 0.755906

		deskjet 0.751816

  ------------
  

+ thinkpad

	+ helios 0.899839

		lifebook 0.894026

		ideapad 0.874554

		ibm 0.86932

		thinkcentre 0.861892

		lenovo 0.856764

		powerbook 0.847202

		qosmio 0.844468

		g4 0.841845

		netbooks 0.841571

  ------------

+ 4s

	+ iphone 0.866726

		3gs 0.799711

		otterbox 0.76216

		defender 0.749466

		commuter 0.745183

		fitted 0.738256

		shell 0.695319

		speck 0.693079

		ipadTM 0.688701

		angry 0.678816

  ------------

+ wii

	+ nintendo 0.891173

		ds 0.829812

		mysims 0.800584

		rabbids 0.785034

		sega 0.783087

		resort 0.780826

		rayman 0.78044

		tennis 0.779597

		showdown 0.773833

		challenge 0.764564

  ------------

+ kindle

	+ amazon 0.92865

		kobo 0.886377

		readers 0.857235

		jivo 0.856378

		timbuk2 0.835876

		easel 0.820328

		nookcolor 0.819258

		bodhi 0.816196

		nook 0.81366

		barnes 0.804153

------------

+ pavilion

	+ sempronTM 0.895489

		phenomTM 0.895455

		hpe 0.893858

		argento 0.859879

		10gb 0.857715

		p7 0.856228

		athlonTM 0.847047

		helios 0.845957

		h8 0.842021

		s5 0.83936

------------

+ 128gb

	+ 256gb 0.968549

		ultrabook 0.952139

		portege 0.878426

		20gb 0.853602

		nero 0.851311

		maxtor 0.851151

		ideapad 0.841534

		desktops 0.835749

		mars 0.833428

		biscotti 0.832344

------------

+ 1080p

	+ 240hz 0.946196

		120hz 0.936596

		viera 0.934346

		600hz 0.930349

		regza 0.920715

		aquos 0.915076

		hdtv 0.91374

		60hz 0.900863

		xbr 0.895103

		720p 0.888174

  ------------

+ 4g

	+ lte 0.886591

		atrix 0.88038

		nexus 0.874014

		htc 0.872857

		verizon 0.87204

		sprint 0.871053

		torch 0.857578

		pantech 0.856833

		droid 0.855748

		huawei 0.84794

------------

+ black

	+ white 0.689792

		silver 0.651717

		gray 0.589055

		red 0.577056

		blue 0.527066

		pink 0.496994

		stainless 0.493225

		ge 0.488674

		biscuit 0.479472

		bisque 0.477485

------------

+ wireless

	+ 11b 0.668098

		mimo 0.657844

		rangebooster 0.655607

		amped 0.654409

		11g 0.65158

		presenter 0.639741

		rangemax 0.632898

		802 0.631181

		dsl 0.629025

		router 0.623429