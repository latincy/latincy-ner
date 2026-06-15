# Calibration review — UD gold-test conflicts (model vs Claude)

Per row mark a verdict (PERSON / LOC / NORP / NONE). Or ratify the class rule at the top of each section and only mark the exceptions.

Total: 72 conflicts across Perseus+PROIEL+UDante test.

## PERSON → LOC · Toponym over-personified — recommend LOC  (21)
_Rule:_ Place-names (cities, rivers, mountains, seas) = LOC even when personifiable; PERSON only if the place acts as a deity in context.

| # | surface | context | model | claude | rec | verdict |
|---|---|---|---|---|---|---|
| 1 | `Lauini` | In regna «Lauini» Dardanidae uenient; | PERSON | LOC | **LOC** |  |
| 2 | `Xanthus` | Non Simois tibi, nec «Xanthus», nec Dorica castra defuerint; | PERSON | LOC | **LOC** |  |
| 3 | `Aornon` | unde locum Grai dixerunt nomine «Aornon». | PERSON | LOC | **LOC** |  |
| 4 | `Lycaei` | …latebris horrenda ferarum et cum Cyllene gelidi pineta «Lycaei»: | PERSON | LOC | **LOC** |  |
| 5 | `Peneidas` | …s expalluit illa citae que uicta labore fugae spectans «Peneidas» undas ' fer pater ' inquit ' opem si flumina numen hab… | PERSON | LOC | **LOC** |  |
| 6 | `Apidanus` | …r parentem, populifer Sperchios et inrequietus Enipeus «Apidanus» que senex lenis que Amphrysos et Aeas, mox que amnes a… | PERSON | LOC | **LOC** |  |
| 7 | `Philadelphiae` | et angelo «Philadelphiae» ecclesiae scribe . | PERSON | LOC | **LOC** |  |
| 8 | `Amaltheam` | ego enim te arbitror caesis apud «Amaltheam» tuam uictimis statim esse ad Sicyonem oppugnandum prof… | PERSON | LOC | **LOC** |  |
| 9 | `Miseni` | τοποθεσίαν quam postulas «Miseni» et Puteolorum includam orationi meae . | PERSON | LOC | **LOC** |  |
| 10 | `Amalthea` | si quies dabitur ab «Amalthea» te non commouebo . | PERSON | LOC | **LOC** |  |
| 11 | `Florentiam` | …scibus equor, quanquam Sarnum biberimus ante dentes et «Florentiam» adeo diligamus ut, quia dileximus, exilium patiamur in… | PERSON | LOC | **LOC** |  |
| 12 | `Apenini` | a meridie quoque Prouincialibus et «Apenini» deuexione clauduntur. | PERSON | LOC | **LOC** |  |
| 13 | `Strate Maioris` | …es, ut Bononienses Burgi Sancti Felicis et Bononienses «Strate Maioris». | PERSON | LOC | **LOC** |  |
| 14 | `Apenini` | …at de linea diuidente, breuiter respondemus esse iugum «Apenini», quod, ceu fistule culmen hinc inde ad diuersa stillic… | PERSON | LOC | **LOC** |  |
| 15 | `Ducatus` | Et dextri regiones sunt Apulia, sed non tota, Roma, «Ducatus», Tuscia et Ianuensis Marchia; | PERSON | LOC | **LOC** |  |
| 16 | `Uenetiis` | …onitana, Romandiola, Lombardia, Marchia Triuisiana cum «Uenetiis». | PERSON | LOC | **LOC** |  |
| 17 | `Anconitane Marchie` | Post hos incolas «Anconitane Marchie» decerpamus, qui Chignamente state siate locuntur: cum … | PERSON | LOC | **LOC** |  |
| 18 | `Apenini` | Transeuntes nunc humeros «Apenini» frondiferos leuam Ytaliam contatim uenemur ceu solemus… | PERSON | LOC | **LOC** |  |
| 19 | `Uerone` | …ordellus de Mantua sua ostendit, Cremone, Brixie atque «Uerone» confini: qui, tantus eloquentie uir existens, non solu… | PERSON | LOC | **LOC** |  |
| 20 | `Aquino` | Renaldus de «Aquino»: Per fino amore uo si letamente; | PERSON | LOC | **LOC** |  |
| 21 | `Marsilia` | Folquetus de «Marsilia»: Tan m'abellis l'amoros pensamen; | PERSON | LOC | **LOC** |  |

## PERSON → NORP · Demonym read as a name — recommend NORP  (18)
_Rule:_ Substantivized demonyms/ethnonyms = NORP, never PERSON, even capitalized.

| # | surface | context | model | claude | rec | verdict |
|---|---|---|---|---|---|---|
| 22 | `Lycaoniae` | … arce, ingemit et, facto nondum uulgata recenti, foeda «Lycaoniae» referens conuiuia mensae, ingentes animo et dignas Iou… | PERSON | NORP | **NORP** |  |
| 23 | `Arcadis` | «Arcadis» hinc sedes et inhospita tecta tyranni ingredior, trahe… | PERSON | NORP | **NORP** |  |
| 24 | `Atticum` | Mel «Atticum» ut domi nasceretur, apes ab Athenis iussit afferri; | PERSON | NORP | **NORP** |  |
| 25 | `Atticum` | uuam passam et mel «Atticum». | PERSON | NORP | **NORP** |  |
| 26 | `Homeristae` | Ipse Trimalchio in puluino consedit, et cum «Homeristae» Graecis uersibus colloquerentur, ut insolenter solent,… | PERSON | NORP | **NORP** |  |
| 27 | `Alexandrinus` | Interim puer «Alexandrinus», qui caldam ministrabat, luscinias coepi imitari clama… | PERSON | NORP | **NORP** |  |
| 28 | `Aegyptio` | … et fecit ultionem ei qui iniuriam sustinebat percusso «Aegyptio» . | PERSON | NORP | **NORP** |  |
| 29 | `Israhel` | hic est Moses qui dixit filiis «Israhel» . | PERSON | NORP | **NORP** |  |
| 30 | `Canusinus` | alteram quam mihi «Canusinus» tuus hospes reddidit . | PERSON | NORP | **NORP** |  |
| 31 | `Lycurgei` | nos met ipsi qui «Lycurgei» a principio fuissemus cotidie demitigamur . | PERSON | NORP | **NORP** |  |
| 32 | `Arpinatium` | «Arpinatium» fremitus est incredibilis de Laterio . | PERSON | NORP | **NORP** |  |
| 33 | `Yspani` | …alii oc alii oïl, alii si affirmando locuntur, ut puta «Yspani», Franci et Latini. | PERSON | NORP | **NORP** |  |
| 34 | `Fauentini` | …enere gentis, ut Neapoletani et Caetani, Rauennates et «Fauentini», et, quod mirabilius est, sub eadem ciuilitate morante… | PERSON | NORP | **NORP** |  |
| 35 | `Triuisianis` | …andiolis, Romandiolorum cum Lombardis, Lombardorum cum «Triuisianis» et Uenetis, horum cum Aquilegiensibus, et istorum cum … | PERSON | NORP | **NORP** |  |
| 36 | `Ystrianis` | … et Uenetis, horum cum Aquilegiensibus, et istorum cum «Ystrianis». | PERSON | NORP | **NORP** |  |
| 37 | `Florentinus` | …unam uidimus recte atque perfecte ligatam, quam quidam «Florentinus» nomine Castra posuerat; | PERSON | NORP | **NORP** |  |
| 38 | `Yspani` | Hoc etiam «Yspani» usi sunt - et dico Yspanos qui poetati sunt in uulgari… | PERSON | NORP | **NORP** |  |
| 39 | `Florentini` | …etur assumptum, sicut inueniri potest in illa Guidonis «Florentini» Donna me prega, et in illa quam diximus Poscia ch'Amor… | PERSON | NORP | **NORP** |  |

## LOC → NORP · Metonymy, people-form — recommend NORP  (15)
_Rule:_ People-form (-i/-es nom.pl., -orum/-um gen.pl., demonym adjective) = NORP.

| # | surface | context | model | claude | rec | verdict |
|---|---|---|---|---|---|---|
| 40 | `Dardanidae` | In regna Lauini «Dardanidae» uenient; | LOC | NORP | **NORP** |  |
| 41 | `Latiis` | tu ducibus «Latiis» aderis, cum laeta triumphum uox canet et uisent longas… | LOC | NORP | **NORP** |  |
| 42 | `Indos` | …thera mente, Aethiopasque suos positos que sub ignibus «Indos» sidereis transit patrios que adit inpiger ortus. | LOC | NORP | **NORP** |  |
| 43 | `Tyria` | …erdidit, quae mihi natali meo cliens quidam donauerat, «Tyria» sine dubio, sed iam semel lota. | LOC | NORP | **NORP** |  |
| 44 | `Chiam` | Cum adhuc capillatus essem, nam a puero uitam «Chiam» gessi, ipsimi nostri delicatus decessit, mehercules ma… | LOC | NORP | **NORP** |  |
| 45 | `Iuda` | ecce uicit leo de tribu «Iuda» radix Dauid aperire librum et septem signacula eius . | LOC | NORP | **NORP** |  |
| 46 | `Epiroticis` | ita neque Achaicis hominibus neque «Epiroticis» paulo liberiores litteras committere audeo . | LOC | NORP | **NORP** |  |
| 47 | `Ungarorum` | Ab isto incipiens ydiomate, uidelicet a finibus «Ungarorum» uersus orientem, aliud occupauit totum quod ab inde uo… | LOC | NORP | **NORP** |  |
| 48 | `Sardis` | …m cum Tuscis, Tuscorum cum Ianuensibus, Ianuensium cum «Sardis»; | LOC | NORP | **NORP** |  |
| 49 | `Lombardis` | … Anconitanis, horum cum Romandiolis, Romandiolorum cum «Lombardis», Lombardorum cum Triuisianis et Uenetis, horum cum Aqu… | LOC | NORP | **NORP** |  |
| 50 | `Latiis` | Sardos etiam, qui non Latii sunt sed «Latiis» associandi uidentur, eiciamus, quoniam soli sine propr… | LOC | NORP | **NORP** |  |
| 51 | `Apuli` | «Apuli» quoque uel sui acerbitate uel finitimorum suorum conti… | LOC | NORP | **NORP** |  |
| 52 | `Apuli` | …lzera che chiangesse lo quatraro Sed quamuis terrigene «Apuli» loquantur obscene comuniter, prefulgentes eorum quidam… | LOC | NORP | **NORP** |  |
| 53 | `Lombardorum` | …ero et Mutinensibus aliqualem garrulitatem que proprie «Lombardorum» est: | LOC | NORP | **NORP** |  |
| 54 | `Lombardi` | …i sunt in Ytalia, ut Siculi, Apuli, Tusci, Romandioli, «Lombardi» et utriusque Marchie uiri. | LOC | NORP | **NORP** |  |

## NORP → LOC · Metonymy, place-form — recommend LOC  (7)
_Rule:_ Singular toponym = LOC.

| # | surface | context | model | claude | rec | verdict |
|---|---|---|---|---|---|---|
| 55 | `Claros` | Mihi Delphica tellus et «Claros» et Tenedos Patarea que regia seruit, Iuppiter est geni… | NORP | LOC | **LOC** |  |
| 56 | `Romandiola` | sinistri autem pars Apulie, Marchia Anconitana, «Romandiola», Lombardia, Marchia Triuisiana cum Uenetiis. | NORP | LOC | **LOC** |  |
| 57 | `Pisa` | «Pisa»ni: Bene andonno li fanti de Fiorensa per Pisa. | NORP | LOC | **LOC** |  |
| 58 | `Belnui` | Namericus de «Belnui»: Nuls hom non pot complir addreciamen; | NORP | LOC | **LOC** |  |
| 59 | `Nauarre` | Rex «Nauarre»: Ire d'amor que en mon cor repaire; | NORP | LOC | **LOC** |  |
| 60 | `Belnui` | Namericus de «Belnui»: Nuls hom non pot complir adrecciamen. | NORP | LOC | **LOC** |  |
| 61 | `Ghisileriis` | … inuenimus, uidelicet Guidonem Guinizelli, Guidonem de «Ghisileriis» et Fabrutium Bononienses: Di fermo sofferire, et Donna… | NORP | LOC | **LOC** |  |

## LOC → PERSON · Place vs named individual — JUDGMENT  (7)
_Rule:_ Named individual / personified actor = PERSON; bare toponym = LOC.

| # | surface | context | model | claude | rec | verdict |
|---|---|---|---|---|---|---|
| 62 | `Peneus` | Per quae «Peneus» ab imo effusus Pindo spumosis uoluitur undis, deiectu … | LOC | PERSON | **?** |  |
| 63 | `Iudam` | …t Thomam Iacobum Alphei et Simonem qui uocatur Zelotes «Iudam» Iacobi et Iudam Scarioth qui fuit proditor . | LOC | PERSON | **?** |  |
| 64 | `Iudam Simonis Scariotis` | dicebat autem «Iudam Simonis Scariotis» . | LOC | PERSON | **?** |  |
| 65 | `Castra` | …atque perfecte ligatam, quam quidam Florentinus nomine «Castra» posuerat; | LOC | PERSON | **?** |  |
| 66 | `Sordellus de Mantua` | … sicut facere quoslibet a finitimis suis conicimus, ut «Sordellus de Mantua» sua ostendit, Cremone, Brixie atque Uerone confini: qu… | LOC | PERSON | **?** |  |
| 67 | `Columpnis` | Iudex de «Columpnis» de Messana: Amor, che lungiamente m'hai menato; | LOC | PERSON | **?** |  |
| 68 | `Totila` | …e florum de sinu tuo, Florentia, nequicquam Trinacriam «Totila» secundus adiuit”. | LOC | PERSON | **?** |  |

## NORP → PERSON · Group vs named individual — recommend PERSON  (4)
_Rule:_ Named individual = PERSON.

| # | surface | context | model | claude | rec | verdict |
|---|---|---|---|---|---|---|
| 69 | `Phileros` | Haec «Phileros» dixit, illa Ganymedes: | NORP | PERSON | **PERSON** |  |
| 70 | `Gallum Pisanum` | …m se ad curiale uulgare direxit, Bonagiuntam Lucensem, «Gallum Pisanum», Minum Mocatum Senensem, Brunectum Florentinum, quorum… | NORP | PERSON | **PERSON** |  |
| 71 | `Minum Mocatum Senensem` | …uulgare direxit, Bonagiuntam Lucensem, Gallum Pisanum, «Minum Mocatum Senensem», Brunectum Florentinum, quorum dicta, si rimari uacaue… | NORP | PERSON | **PERSON** |  |
| 72 | `Cynum Pistoriensem` | …cilicet Guidonem, Lapum et unum alium, Florentinos, et «Cynum Pistoriensem», quem nunc indigne postponimus, non indigne coacti. | NORP | PERSON | **PERSON** |  |
