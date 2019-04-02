# Analiza tvitov Ruskih trolov (vmesno poročilo)

## Avtorji
* Žan Bizjak
* Gašper Mrak
* Matej Fajdiga
* Uroš Koritnik
* Jakob Kovačič

## Opis problema
Za projekt pri predmetu smo smo si izbrali podatkovo analizo tvitov Ruskih "trolov", s katerimi naj bi Rusija vplivala na Ameriške volitve. Začetne podatke bomo pridobili preko spletne strani Kaggle in sicer dve .csv datoteki, ena z tviti, druga z računi trolov. Analizirali bomo vsebine tvitov, lastnosti računov in preko tega poskusili ugotovite razne vzorce v objavah - najpogostejše fraze, prevadujoče "heštege", ciljne skupine, časovne intervale ipd. Hkrati bi tudi lahko vpeljali tvite in račune dejanskih uporabnikov in primerjali rezultate in tako morda ugotovili ključne razlike med njima.

## Podatki
Začetni vir podatkov: https://www.kaggle.com/vikasg/russian-troll-tweets

## Analiza

## Časovna porazdelitev uporabnikov in tweetov

Podatke smo pridobili s Kaggla, in sicer dve csv datoteke "tweets" in "users". Relacijsko se povezujejo preko attributa "user_id". Datoteka "tweets" vsebuje tudi attribut "tweet_id", s katerim lahko tudi pregledujemo medsebojno povezanost tweetov trolov. Preko te informacije in s predpostavko, da se v teh tweetih nahajajo le troli, lahko ugotovimo ali so ciljali na uporabnike izven naših podatkov, ali so tweete razširjali in popularizirali le med seboj.

Problem v podatkih je tudi, da najstarejši tweet seže le do julija 2014 ampak najstarejši uporabnik pa vse do januarja 2009. Z izrisom grafov porazdelitve tweetov in nastanka računov po času lahko vidimo z metodo ostrega očesa, da se gostota periodično viša.

<img href='./Images/Figure_2.png'>

Graf prikazuje število ustvarjenih računov glede na mesec. Opazimo dva izrazita vrhova v porazdelitvi in eno kasnejše izstopanje. Z uporabo Wikipedijinega portala Current Events smo poskušali povezati vrhove s svetovnimi dogodki in smo prišli do ugotovitve, da sovpadajo s glavnimi Ruskimi političnimi potezami in sicer:

Začetek prvega izstopanja sovpada s Snowdenovim priznanjem "žvižgaštva" zaupnih dokumentov NSA in začetkom raziskave uporabe kemičnega orožja v Siriji. Vrh doseže ko Snowdnu podeli Rusija azil in na vrhuncu raziskave v Siriji.

Drugo izstopanje sovpada s Krimsko krizo, v kateri si je Rusija priključila polotok. Natančnih dogodkov, poleg priključitve, nismo zasledili.

Zadnje izstopanje sovpada s začetkom partijskih volitev v ZDA, kjer naj bi troli imeli vlogo pri izvolitvi Donalda Trumpa. Zaradi nizkega števila prijavljenjih računov pa je možno da nanj gledamo tudi kot osamelec, saj so prejšnji vzorci vrhov vsebovali vsaj štiri zaporedne mesce povečanega števila računov skupaj s izrazitim vrhom.

<img href='./Images/Figure_3.png'>

Graf prikazuje število objavljenih tweetov glede na mesec. Razberemo lahko tri obdobja povečanega tweetanja. Podobno kot zgoraj smo poiskali sovpadanja s svetovnimi dogodki.

Prvo obdobje sovpada s Ameriškimi sankcijami na Severno Korejo ter s terrorističnim napadom na Francoski satirični tednik Charlie Hebdo.

Drugo obdobje se ne sovpada s svetovnimi dogodki, ampak zdi se, da število tweetov narašča s naraščajočo priljubljenostjo Donalda Trumpa in njegovo kandidaturo.

Tretje obdobje sovpada z začetkom partisjskih volitev v ZDA, podobno kakor v prejšnjem grafu. Dogodka odgovorna za vrhova sta predsedniška debata med Donaldom Trumpom in Hillary Clinton, ter škandal slednje glede njenega upravlanja zaupnih dokumentov medtem, ko je bila zaposlena v Beli Hiši.

## Hashtagi

Hashtagi so osrednji način za označevanje tematik na Twitterju. Preko njih lahko razberemo ne le tematiko, ampak tudi opredeljenost uporabnika glede nje. Služijo lahko kot preprosto izhodišče za nenadzorovano učenje, za razliko od tekstovne analize celotnega tweeta. Preko najdenih skupin uporabnikov bomo lahko nato razbrali vzorce delovanja trolov, najpogostejše citirane medije, fraze, "false flag" napade... .

<img href='./Images/Figure_1.png'>

Osnovni graf hashtagov glede na število prikazuje porazdelitev najpogostejših desetih hashtagov. Najzanimiveša sta #pjnet in #MerkelMussBleiben. Prvi je okrajšava za Patriot Journalist Network, družba katera je med volitvami na Twitterju vzdrževala bota, ki naj bi vsak dan objavil tisoč tweetov.
Slednja pa namiguje, da so troli tudi komentirali zadeve izven Ameriške sfere.
