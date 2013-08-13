#############################################################################################
# HTTP Anidb Metadata Agent (HAMA) # v0.4 for plex # By Atomicstrawberry # Forked by ZeroQI #
#############################################################################################

  ### Functionality change
  #   . Local (anime-titles.xml) Title XML Title & Keyword parsing: search main title or any language in the language order.
  #   . Local (anime-list-full.xml) theTVDB lookup table through mapping XML, WAY more covers (no more title search)
  #   . Versatile search: can manage colon replaced by double tilde, split words incorrectly, with missing dash without renaming folder
  #   . International language support, not only english.
  #   . Reduced the number of functions and improved overall source code clarity
  #
  ### Bug improvement
  #   . Fork Commas in "DefaultPrefs.json" prevented to see settings in Settings > Tab: Plex Media Server > Sidebar: Agents > Tab: Movies/TV Shows > Tab HamaTV
  #   . Search page couldn't find some anime despite exact title (could be gotten around using leading backslash '\').
  #
  ### Roadmap
  #   . To Do:   
  #              Local file lookup
  #               - "aidxxxxx.jpg" cover with AnimeID as title
  #               - "AniDB.ID"     file containing id
  #               - "AniDB.NFO"    containing XML from anidb. when refreshing it or when otion enabled save it localy ?

  ### Flow of information and functions                                 Local                  Web
  #
  #searchByName   (results, lang,   origTitle, year )
  #    xmlElementFromFile(ANIDB_ANIME_TITLES, ANIDB_ANIME_TITLES_URL)   anime-titles.xml   
  #
  #  ###aid:xxxx
  #    getMainTitle      (titles, LANGUAGE_PRIORITY)
  #  ###Exact match
  #    cleanse_title     (origTitle)
  #    getMainTitle      (titles, LANGUAGE_PRIORITY)
  #  ###keyword match
  #    splitByChars      (origTitle, SPLIT_CHARS)
  #    cleanse_title     (origTitle)
  #    getScore          (a, b)
  #    getMainTitle      (titles, LANGUAGE_PRIORITY)
  #
  #parseAnimeXml
  #    getResultFromAnidb(ANIDB_HTTP_API_URL + animeID)                                     Anime xml to string
  #    searchInTVDB      (metadata):                                                        anime-list-full.xml
  #    getImagesFromTVDB (metadata, tvdbSeriesId)

### Preferences declared in "DefaultPrefs.json", accessible in Settings > Tab: Plex Media Server > Sidebar: Agents > Tab: Movies/TV Shows > Tab HamaTV ###
#Prefs['GetTvdbFanart'    ] "id": "GetTvdbFanart",     "label": "Attempt to fetch Fanart images from TVDB",               "type": "bool", "default": "true"
#Prefs['GetTvdbPosters'   ] "id": "GetTvdbPosters",    "label": "Attempt to fetch Poster images from TVDB",               "type": "bool", "default": "true"
#Prefs['GetTvdbBanners'   ] "id": "GetTvdbBanners",    "label": "Attempt to fetch series Banner images from TVDB",        "type": "bool", "default": "true"
#Prefs['PreferAnidbPoster'] "id": "PreferAnidbPoster", "label": "Prefer AniDB's poster over TVDB if TVDB lookup enabled", "type": "bool", "default": "false"
##Prefs['
##Prefs['

SERIE_LANGUAGE_PRIORITY   = [ 'x-jat', 'en']
EPISODE_LANGUAGE_PRIORITY = [ 'en', 'x-jat']
FILTER_CHARS              = "\\/:*?<>|~- "
SPLIT_CHARS               = [';', ',', '.', '~', '-' ] #Space is implied
HTTP.CacheTime            = CACHE_1HOUR * 26
SECONDS_BETWEEN_REQUESTS  = 2

### AniDB and TVDB URL and path variable definition ####################################################################################################################
TVDB_API_KEY                 = 'A27AD9BE0DA63333'                                              # TVDB API key register URL: http://thetvdb.com/?tab=apiregister
TVDB_BANNERS_URL             = 'http://thetvdb.com/api/%s/series/%s/banners.xml'               # TVDB Serie pictures xml: fanarts, posters, banners   
TVDB_IMAGES_URL              = 'http://thetvdb.com/banners/'                                   # TVDB picture directory
TVDB_HTTP_API_URL            = 'http://thetvdb.com/api/%s/series/%s/all/en.xml'                # TVDB Serie XML for episodes sumaries for now

ANIDB_HTTP_API_URL           = 'http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid='
ANIDB_PIC_BASE_URL           = 'http://img7.anidb.net/pics/anime/'                             # AniDB picture directory
ANIDB_ANIME_TITLES_URL       = 'http://anidb.net/api/anime-titles.xml.gz'                      # AniDB title database file contain all ids, all languages
ANIDB_ANIME_TITLES           = 'anime-titles.xml'                                              # AniDB title database decompressed in Hama.bundle\Contents\Resources

ANIDB_TVDB_MAPPING           = 'anime-list-full.xml'                                           # ScudLee AniDB to TVDB XML mapping file
ANIDB_TVDB_MAPPING_URL       = 'https://raw.github.com/ScudLee/anime-lists/master/anime-list-full.xml'
ANIDB_COLLECTION_MAPPING     = 'anime-movieset-list.xml'                                       # ScudLee AniDB movies collections XML mapping file
ANIDB_COLLECTION_MAPPING_URL = 'https://github.com/ScudLee/anime-lists/raw/master/anime-movieset-list.xml'

# ScudLee mapping files
#######################
#
# Source:                      Git Dev repository: https://github.com/ScudLee/anime-lists
#                              Dev Forum thread:   http://forum.xbmc.org/showthread.php?tid=142835 - XBMC Anidb.net MOD plugin
#                               
# anime-list-todo.xml        - This is a list of shows that don't yet have a mapping.
#                              In a lot of cases they just need the tvdbid and defaulttvdbseason (and/or imdbid/tmdbid).
#                              More complicated ones may need individual episode mappings (particularly for OVAs linked to TV series).
#                              Some of the shows are deliberately left out because the episodes were a mess on thetvdb when I looked,
#                              but they may have been fixed since then (the scraper should still manage to find artwork without a mapping).
#
# anime-list-unknown.xml     - This is a list of shows he couldn't find on thetvdb when he looked for them.
#
# anime-movieset-list.xml    - Still needs a lot of work. The format should be fairly obvious. 
#                              "Official" collection titles for languages other than English need to be added...
#                              Hentai titles are almost entirely missing...
#                              Any recent movies/OVAs might be missing (he wrote the list a while back, and only did a minor update before posting it)... 
#
# Help the XML Updated?        http://forum.xbmc.org/showthread.php?tid=142835&pid=1432010#pid1432010
#                              if you do one or two shows, PM me (ScudLee), so as not to flood the thread with posts
#                              if you do a whole batch, post it in the thread link indicated above
#                              If you're familiar with Git and GitHub, 1) you can also clone ScudLee repo, edit your copy of anime-list-master.xml directly
#                              and then make a Pull Request (@vaneska does it this way). That simplifies things greatly for me, but is a bit technical.
#
#                                    

### List of AniDB category names useful as genre. 1st variable mark 18+ categories. The 2nd variable will actually cause a flag to appear in Plex ######################
RESTRICTED_GENRE_NAMES    = [ '18 Restricted', 'Pornography' ]
RESTRICTED_CONTENT_RATING = "NC-17"
GENRE_NAMES               = [

  ### Audience categories - all useful but not used often ############################################################################################################
  'Josei', 'Kodomo', 'Mina', 'Seinen', 'Shoujo', 'Shounen',
  
  ### Elements - many useful #########################################################################################################################################
  'Action', 'Martial Arts', 'Swordplay', 'Adventure', 'Angst', 'Anthropomorphism', 'Comedy', 'Parody', 'Slapstick', 'Super Deformed', 'Detective', 'Ecchi', 'Fantasy',
  'Contemporary Fantasy', 'Dark Fantasy', 'Ghost', 'High Fantasy', 'Magic', 'Vampire', 'Zombie', 'Harem', 'Reverse Harem', 'Henshin', 'Horror', 'Incest',
  'Mahou Shoujo', 'Pornography', 'Yaoi', 'Yuri', 'Romance', 'Love Polygon', 'Shoujo Ai', 'Shounen Ai', 'Sci-Fi', 'Alien', 'Mecha', 'Space Travel', 'Time Travel', 
  'Thriller', 'Western',                                             
      
  ### Fetishes. Leaving out most porn genres #########################################################################################################################
  'Futanari', 'Lolicon', 'Shotacon', 'Tentacle', 'Trap', 'Reverse Trap',
  
  ### Original Work - mainly useful ##################################################################################################################################
  'Game', 'Action Game', 'Dating Sim - Visual Novel', 'Erotic Game', 'RPG', 'Manga', '4-koma', 'Movie', 'Novel',
  
  ### Setting - most of the places aren't genres, some Time stuff is useful ##########################################################################################
  'Fantasy World', 'Parallel Universe', 'Virtual Reality', 'Hell', 'Space', 'Mars', 'Space Colony', 'Shipboard', 'Alternative Universe', 'Past', 'Present', 'Future',
  'Historical', '1920s', 'Bakumatsu - Meiji Period', 'Edo Period', 'Heian Period', 'Sengoku Period', 'Victorian Period', 'World War I', 'World War II',
  'Alternative Present',
  
  ### Themes - many useful ###########################################################################################################################################
  'Anti-War', 'Art', 'Music', 'Band', 'Idol', 'Photography', 'Christmas', 'Coming of Age', 'Conspiracy', 'Cooking', 'Cosplay', 'Cyberpunk', 'Daily Life', 'Earthquake',
  'Post-War', 'Post-apocalypse', 'War', 'Dystopia', 'Friendship', 'Law and Order', 'Cops', 'Special Squads', 'Military', 'Airforce', 'Feudal Warfare', 'Navy',
  'Politics', 'Proxy Battles', 'Racism', 'Religion', 'School Life', 'All-boys School', 'All-girls School', 'Art School', 'Clubs', 'College', 'Delinquents', 
  'Elementary School', 'High School', 'School Dormitory', 'Student Council', 'Transfer Student', 'Sports', 'Acrobatics', 'Archery', 'Badminton', 'Baseball', 
  'Basketball', 'Board Games', 'Chess', 'Go', 'Mahjong', 'Shougi', 'Combat', 'Boxing', 'Judo', 'Kendo', 'Muay Thai', 'Wrestling', 'Cycling', 'Dodgeball', 'Fishing',
  'Football', 'Golf', 'Gymnastics', 'Horse Riding', 'Ice Skating', 'Inline Skating', 'Motorsport', 'Formula Racing', 'Street Racing', 'Rugby', 'Swimming', 'Tennis',
  'Track and Field', 'Volleyball', 'Steampunk', 'Summer Festival', 'Tragedy', 'Underworld', 'Assassin', 'Bounty Hunter', 'Mafia', 'Yakuza', 'Pirate', 'Terrorist',
  'Thief'
]

### These are words which cause extra noise due to being uninteresting for doing searches on ###########################################################################
FILTER_SEARCH_WORDS = [                                                                                                          # Lowercase only
    'a',  'of', 'an', 'the', 'motion', 'picture', 'special', 'oav', 'tv', 'special', 'eternal', 'final', 'last', 'one', 'movie', # En particles
    'to', 'wa', 'ga', 'no', 'age', 'da', 'chou', 'super', 'yo', 'de',                                                            # Jp particles
    'le', 'la', 'un', 'les', 'nos', 'vos', 'des', 'ses'                                                                          # Fr particles
]

### set up some stuff ###
import os, os.path, re, time, datetime
# Functions used per module: os (read), re (sub, match), time (sleep), datetim (datetime).
# Unused modules: urllib, types, hashlib , unicodedata, Stack, utils

NAME                = "HTTP Anidb Metadata Agent (HAMA) by Atomicstrawberry forked by ZeroQI"
ART                 = 'art-default.jpg'
ICON                = 'icon-default.png'
DirectoryItem.thumb = R(ICON)
MediaContainer.art  = R(ART)
#MediaContainer.title1 = "HTTP Anidb Metadata Agent (HAMA) by Atomicstrawberry forked by ZeroQI"

networkLock = Thread.Lock()
def Start():
  Log.Debug('### HTTP Anidb Metadata Agent (HAMA) Started #################################################################################################')

  # Initialize the plugin
  #Plugin.AddPrefixHandler(VIDEO_PREFIX, MainMenu, NAME, ICON, ART)
  #Plugin.AddViewGroup("List", viewMode = "List", mediaType = "items")

  # Setup the artwork associated with the plugin
  #MediaContainer.viewGroup = "List"
  MediaContainer.art       = R(ART)
  MediaContainer.title1    = NAME
  DirectoryItem.thumb      = R(ICON)

#def Validate Prefs()

### main metadata agent ################################################################################################################################################
class HamaCommonAgent:

  ### Local XML AniDB lookup ###
  def searchByName(self, results, lang, origTitle, year=""):
  
    Log.Debug("=== searchByName - Begin - ================================================================================================")
    Log("SearchByName (%s,%s,%s,%s)" % (results, lang, origTitle, str(year) ))
    tree = self.xmlElementFromFile(ANIDB_ANIME_TITLES, ANIDB_ANIME_TITLES_URL)                #Get the xml title file into a tree, #from lxml import etree #doc = etree.parse('content-sample.xml')
    #Log("SearchByName - %s loaded" % ANIDB_ANIME_TITLES)                                     #Check logs to see loading time
    
    ### aid:xxxxx Fetch the exact serie XML form AniDB.net (Caching it) from the anime-id ###
    if origTitle.startswith('aid:'):
      animeId = str(origTitle[4:])                                                            #Get string after "aid:" which is 4 characters
      Log.Debug( "SearchByName - aid: %s" % animeId)
      langTitle, mainTitle = self.getMainTitle(tree.xpath("/animetitles/anime[@aid='%s']/*" % animeId), LANGUAGE_PRIORITY) #extract titles from the Anime XML element tree directly
      Log.Debug( "SearchByName - aid: %s %s (%s)" % (animeId, langTitle, mainTitle) )
      results.Append(MetadataSearchResult(id=animeId, name=langTitle, year=None, lang=Locale.Language.English, score=100))
      return 
    
    ### Local exact search ###
    #Log.Debug('SearchByName - XML exact search - Trying to match: ' + origTitle)
    cleansedTitle = self.cleanse_title (origTitle)
    elements      = list(tree.iterdescendants())    #from lxml import etree; tree = etree.parse(ANIDB_ANIME_TITLES) folder missing?; #To-Do: Save to local (media OR cache-type folder) XML???  
    for title in elements:
      if title.get('aid'):                                                                    #is an anime tag (not title tag) in that case ###
        aid = title.get('aid')
      else:
        if title.get('{http://www.w3.org/XML/1998/namespace}lang') in SERIE_LANGUAGE_PRIORITY or title.get('type')=='main':
          sample = self.cleanse_title (title.text)
          if cleansedTitle == sample :                                                        #Should i add "origTitle.lower()==title.text.lower() or" ??
            Log.Debug("SearchByName: Local exact search for '%s' matched aid: %s %s" % (origTitle, aid,title.text))
            langTitle, mainTitle = self.getMainTitle(title.getparent(), SERIE_LANGUAGE_PRIORITY)    #Title according language order selection instead of main title
            results.Append(MetadataSearchResult(id=aid, name=langTitle, year=None, lang=Locale.Language.English, score=100))
            return
    
    ### local keyword search ###
    matchedTitles  = [ ]
    words          = [ ]
    temp           = ""
    for word in self.splitByChars(origTitle, SPLIT_CHARS):
      word = self.cleanse_title (word)
      if not word=="" and word not in FILTER_SEARCH_WORDS and len(word)>1:                    #Special characters scrubbed result in empty word matching all
        words.append (word)
        temp += "'%s', " % word
    Log.Debug("SearchByName - XML Keyword search -  Trying to match: '%s' with Keywords: %s " % (origTitle, temp) )

    if len(words)==0 or len( self.splitByChars(origTitle, SPLIT_CHARS) )==1 :                 # Single work title so already tested
      return None                                                                             # No result found
    
    for title in elements:                                                                    # For each line in the XML case
      if title.get('aid'):                                                                    #   If it is an anime tag in that case
        aid = title.get('aid')                                                                #     Save the Animeid
      else:                                                                                   # Else
        if title.get('{http://www.w3.org/XML/1998/namespace}lang') in SERIE_LANGUAGE_PRIORITY or title.get('type')=='main': #
          sample = self.cleanse_title (title.text)                                            # Cleanse 
          for word in words:                                                                  # For each keyword
            if word in sample:                                                                #   if work in cleanse comparison title
              index  = len(matchedTitles)-1                                                   #     find the key of last elements
              if index >=0 and matchedTitles[index][0] == aid:                                #     if same serie id and at least an element (update array for same aid)
                if title.get('type') == 'main':                                               #       if main title
                  matchedTitles[index][1] = aid.zfill(5) + ' ' + title.text                   #         use main title as display title as it pass the match as well
                if not title.text in matchedTitles[index][2]:                                 #       if title not already added
                  matchedTitles[index][2].append(title.text)                                  #         append title to allTitles list
              else:                                                                           #     else
                matchedTitles.append([aid, aid.zfill(5) + ' ' + title.text, [title.text] ])   #       new insertion (not necessarily main title)
                #Log.Debug("SearchByName - XML Keyword search - keyword '%s' matched '%s'" % (word, sample) )
    if len(matchedTitles)==0:
      return None

    ### calculate scores + Buid results ###
    for match in matchedTitles:
      scores = []                                                                             
      for title in match[2]:                                                                  # Calculate distance without space and characters not allowed for files 
        scores.append(self.getScore( self.cleanse_title(title), cleansedTitle ))              # (removed tilde when used WRONGLY as separator by MIKE)
      bestScore = max(scores)
      results.Append(MetadataSearchResult(id=match[0], name=match[1], year=None, lang=Locale.Language.English, score=bestScore))
      Log.Debug("SearchByName - %s%% similarity with %s" % ('{:>2}'.format(str(bestScore)), match[1]) )
    results.Sort('score', descending=True)
    Log.Debug("=== searchByName - End - =================================================================================================")
	
  ### Import XML file from 'Resources' folder into an XML element ######################################################################################################
  def xmlElementFromFile (self, filename, url):
    if not ""=="": #if not up to date...
      string = XML.ElementFromURL(ANIDB_ANIME_TITLES_URL, cacheTime=CACHE_1HOUR * 24 * 7);
       # String = XML.ElementFromString( Archive.GzipDecompress( HTTP.Request(subUrl, headers={'Accept-Encoding':''}).content ) )
    else:
      Log('xmlElementFromFile (%s, %s) %s' % (filename, url, R(filename) ) )
      string = Resource.Load(filename) #no option to write
   
    return XML.ElementFromString(string) 

  ### Get the Levenshtein distance score in percent between two strings ################################################################################################
  def getScore(self, a, b):
    return int(100 - (100 * float(Util.LevenshteinDistance(a,b)) / float(max(len(a),len(b))) ))   #To-Do: LongestCommonSubstring(first, second). use that?

  ### Cleanse title of FILTER_CHARS and translate anidb '`' ############################################################################################################
  def cleanse_title(self, title):
    return title.replace("'", "`").translate(None, FILTER_CHARS).lower()

  ### Split a string per list of chars #################################################################################################################################
  def splitByChars(self, string, separators=SPLIT_CHARS):
    
    for i in separators:
      string.replace(" ", i)
    #for i in range(len(string)):
    #  if string[i] in separators:
    #    string[i] = ' '
    return string.split()

  ### extract the series / movie title / Episode title #################################################################################################################################
  def getMainTitle(self, titles, LANGUAGE_PRIORITY):
    
    langTitles = ["" for index in range(len(LANGUAGE_PRIORITY)+2)]                            # LANGUAGE_PRIORITY title order, original title, then choosen title
    for title in titles:                                                                      # For each of the possible titles given
      lang = title.get('{http://www.w3.org/XML/1998/namespace}lang')                          #   Get the language, 'xml:lang' attribute need hack to read properly
      type = title.get('type')                                                                #   Get the type (main, official, syn, short)
                                                                                              
      if type == 'main' or type == None and langTitles[ len(LANGUAGE_PRIORITY) ] == "":       # If main title or default episode title empty
          langTitles [ len(LANGUAGE_PRIORITY)        ] = title.text                           #   save main title or episode first result as original title
      if type in ['official', 'main', None]  and lang in LANGUAGE_PRIORITY:                   # If title in the languages order (include main title)
          langTitles [ LANGUAGE_PRIORITY.index(lang) ] = title.text                           #   save it in the right language slot
                                                                                              
      for index in range( len(LANGUAGE_PRIORITY)+1 ):                                         # Loop all saved language and main titles in the priority order
        if not langTitles [ index ] == '' :                                                   #   If the title for language was filled
          langTitles [len(LANGUAGE_PRIORITY)+1] = langTitles [ index ]                        #     set as language title
          break                                                                               #     Break the loop if found the title
                                                                                               
    if not type== None:
      Log.Debug("getMainTitle (%d titles) Title: %s  Main title: %s" % (len(titles), langTitles[len(LANGUAGE_PRIORITY)], langTitles[len(LANGUAGE_PRIORITY)+1] ))
    return langTitles[len(LANGUAGE_PRIORITY)+1], langTitles[len(LANGUAGE_PRIORITY)]

  ### Parse the AniDB anime XML ########################################################################################################################################
  def parseAniDBXml(self, metadata, media, force, movie):
   
    # -------   -----------------------   ------------------------------------------------------------------------------------------------------------------------------
    # TSEMAGT   Metadata Model Classes    Description - Source: http://dev.plexapp.com/docs/agents/models.html 
    # -------   -----------------------   --------------------------------- --------------------------------------------------------------------------------------------
    # X         class TV_Show             Represents a TV show, or the top -level of other episodic content.
    #  X        class Season              Represents a season of a TV show.
    #   X       class Episode             Represents an episode of a TV show or other episodic content. 
    #    X      class Movie               Represents a movie (e.g. a theatrical release, independent film, home movie, etc.)
    #     X     class Album               Represents a music album.
    #      X    class Artist              Represents an artist or group.
    #       X   Track                     Represents an audio track (e.g. music, audiobook, podcast, etc.)   
    # -------   -----------------------   ------------------------------------------------------------------------------------------------------------------------------
    # X.XXXX.   title                     A string specifying the title.
    # XXXXXX.   summary                   A string specifying the summary.
    # X.XXX..   originally_available_at   A date object specifying the movie/episode’s original release date.
    # X..X...   duration                  An integer specifying the duration of the movie, in milliseconds.
    # ..X....   absolute_index            An integer specifying the absolute index of the episode within the entire series.
    # ...XX..   original_title            A string specifying the original title.
    # ...X...   tagline                   A string specifying the tagline.
    # ...X...   year                      An integer specifying the movie’s release year.
    # ......X   name                      A string specifying the track’s name.
    # .X.....   episodes                  A map of Episode objects.
    # ....X..   tracks                    A map of Track objects.
    #--------   -----------------------   ------------------------------------------------------------------------------------------------------------------------------
    # X..XX..   studio                    A string specifying the studio.
    # X..XX..   countries                 A set of strings specifying the countries involved in the production of the movie.
    # ..XX...   writers                   A set of strings specifying the writers.
    # ..XX...   directors                 A set of strings specifying the directors.
    # ..XXX..   producers                 A set of strings specifying the producers. 
    # -------   -----------------------   ------------------------------------------------------------------------------------------------------------------------------
    # X.XXXX.   rating                    A float between 0 and 10 specifying the movie/episode’s rating.
    # X..XXX.   genres                    A set of strings specifying the movie’s genre.
    # X..XXX.   tags                      A set of strings specifying the movie’s tags.
    # X..XXX.   collections               A set of strings specifying the movie’s genre.
    # X..X...   content_rating            A string specifying the movie’s content rating.
    # ...X...   content_rating_age        A string specifying the minumum age for viewers of the movie.
    # ...X...   trivia                    A string containing trivia about the movie.
    # ...X...   quotes                    A string containing memorable quotes from the movie.
    # -------   -----------------------   ------------------------------------------------------------------------------------------------------------------------------
    # X..X.X.   art                       A container of proxy objects representing the movie’s background art. See below for information about proxy objects.
    # XX.XXX.   posters                   A container of proxy objects representing the movie’s posters. See below for information about proxy objects.
    # XX.....   banners                   A container of proxy objects representing the season’s banner images. See below for information about proxy objects.
    # ..X....   thumbs                    A container of proxy objects representing the episode’s thumbnail images. See below for information about proxy objects.
    # X..X.X.   themes                    A container of proxy objects representing the movie’s theme music. See below for information about proxy objects.
    # -------   -----------------------   ------------------------------------------------------------------------------------------------------------------------------
  
    PreferAnidbPoster = Prefs['PreferAnidbPoster'];
    GetTvdbPosters    = Prefs['GetTvdbPosters'   ];
    GetTvdbFanart     = Prefs['GetTvdbFanart'    ];
    GetTvdbBanners    = Prefs['GetTvdbBanners'   ];
    
    Log.Debug('--- parseAniDBXml - Begin -------------------------------------------------------------------------------------------')
    Log("parseAniDBXml (%s, %s, %s)" % (metadata, media, force) )

    anime          = self.urlLoadXml( ANIDB_HTTP_API_URL + metadata.id ).xpath('/anime')[0]   ### Pull down the XML for a given anime ID. Don't worry about caching, the HTTP system does that ###
    getElementText = lambda el, xp : el.xpath(xp)[0].text if el.xpath(xp)[0].text else ""     # helper for getting text from XML element
    movie          = (True if getElementText(anime, 'type')=='Movie' else False)              # Read movie type from XML
    
    tvdbid, defaulttvdbseason, mappingList, studio = self.anidbTvdbMapping(metadata)          # Search for the TVDB ID from the animeId + update studio
    if tvdbid in ['movie', 'OAV', 'hentai', 'unknown', 'tv special', None]:                   # If a TV Serie so will have a tvdbid
      tvdbid = None
    
    ### Title ###
    try:
      metadata.title, orig = self.getMainTitle(anime.xpath('/anime/titles/title'), SERIE_LANGUAGE_PRIORITY)
    except:
      raise ValueError                                                                        # No title found
    if movie:
      metadata.original_title = orig  #http://forums.plexapp.com/index.php/topic/25584-setting-metadata-original-title-and-sort-title-still-not-possible/
    Log.Debug("parseAniDBXml - Chosen title: '%s' original title: '%s'" % (metadata.title, metadata.original_title))

    ### Summary ###
    try:                                                                                      # Remove wiki-style links to staff, characters etc
      description = "AniDB.net:   <A href='http://anidb.net/perl-bin/animedb.pl?show=anime&aid=%s'>%s</A><BR />\n" % (metadata.id, metadata.title) + \
                    "TheTVDB.com: <A href='http://thetvdb.com/?tab=series&id=%s'>%s</A><BR />\n"                   % (tvdbid,      metadata.title) + \
                    re.sub(r'http://anidb\.net/[a-z]{2}[0-9]+ \[(.+?)\]', r'\1', getElementText(anime, 'description'))
      metadata.summary = description 
    except Exception, e:
      Log.Debug("Exception: " + str(e))
      pass
    
    ### Start date ###
    startdate                          = getElementText(anime, 'startdate')                                           # get start date if any
    if startdate != "":
      metadata.originally_available_at = Datetime.ParseDate(startdate).date()                                       # Update metadata.originally_available_at
      if movie:
        metadata.year = metadata.originally_available_at.year
    
    ### Ratings
    rating = getElementText(anime, 'ratings/permanent')                       
    if rating:
      metadata.rating = float(rating)  
      
    
    ### Category -> Genre mapping ###
    temp              = ""
    genres            = {}
    restrictedContent = False
    for category in anime.xpath('categories/category'):                         
      weight = category.get('weight')
      name   = getElementText(category, 'name')
      if name in GENRE_NAMES:   #and not weigth<MINIMUM_WEIGHT
        genres[name]      = int(weight)
        temp             += name + " "
      if name in RESTRICTED_GENRE_NAMES:
        if not  metadata.content_rating == RESTRICTED_CONTENT_RATING:
          metadata.content_rating = RESTRICTED_CONTENT_RATING
          restrictedContent       = True
        temp             += name + "(18+) "
    sortedGenres = sorted(genres.items(), key=lambda x: x[1],  reverse=True)                  # sort genre list
    if len(sortedGenres) > 6: #remove categories below minimum weight instead
      del sortedGenres[6:]
    
    temp = ""
    metadata.genres.clear()
    for genre in sortedGenres:
      metadata.genres.add(genre[0])
      temp += "%s (%s) " % (genre[0], str(genre[1])) 
    Log.Debug("parseAniDBXml - Categories - Genres (Weight): " + temp) 
      
    ### Posters AniDB.net ###
    if getElementText(anime, 'picture') != "":                                                # If anidb poster exist
      bannerRealUrl = ANIDB_PIC_BASE_URL + getElementText(anime, 'picture');                  #   Build banner RealUrl variable
      if not bannerRealUrl in metadata.posters:                                               #   If url not already there
        metadata.posters[ bannerRealUrl ] = Proxy.Media(HTTP.Request( bannerRealUrl ).content, sort_order=(1 if PreferAnidbPoster else 99))
    
    ### thetvdb.com - Posters + Studio + Episode summary [anime-list-full.xml] ###
    if tvdbid:                                                                                # If a TV Serie so will have a tvdbid

      if GetTvdbPosters or GetTvdbFanart or GetTvdbBanners:                                   # TVDB doesn't index movies, nor 18+ anime
        self.getImagesFromTVDB(metadata, media, tvdbid)                                       # getImagesFromTVDB(self, metadata, tvdbSeriesId):self.getImagesFromTVDB(metadata, media, tvdbid)                                           # getImagesFromTVDB(self, metadata, tvdbSeriesId):
     
      ### thetvdb.com - Build 'tvdbSummary' table ###
      tvdbanime = self.urlLoadXml( TVDB_HTTP_API_URL % (TVDB_API_KEY, tvdbid) ).xpath('/Data')[0] ### Pull down the XML cached if possible for a given anime ID
      tvdbSummary         = {}
      tvdbSummaryAbsolute = {}

      for episode in tvdbanime.xpath('Episode'):                         
        Overview        = getElementText(episode, 'Overview'       )    
        SeasonNumber    = getElementText(episode, 'SeasonNumber'   )   
        EpisodeNumber   = getElementText(episode, 'EpisodeNumber'  )
        absolute_number = getElementText(episode, 'absolute_number')
        EpisodeNumber   = getElementText(episode, 'EpisodeNumber'  )
        id              = getElementText(episode, 'id'             )
        seasonid        = getElementText(episode, 'seasonid'       )
        EpisodeName     = getElementText(episode, 'EpisodeName'    )
        if not SeasonNumber=="" and not EpisodeNumber=="":                                     # If something to treat
          if Overview=="":
            Log.Debug("parseAniDBXml - theTVDB.com Episode Summary missing - " + metadata.title + " s" + SeasonNumber + "e" + EpisodeNumber + " - " + TVDB_HTTP_API_URL % (TVDB_API_KEY, tvdbid))
          Overview = "TheTVDB.com: <A href='http://thetvdb.com/?tab=series&id=%s'                         >%s</A> > "          % (tvdbid, metadata.title                           ) + \
                                  "<A href='http://thetvdb.com/?tab=season&seriesid=%s&seasonid=%s'       >Season %s</A> > "   % (tvdbid, seasonid, SeasonNumber                   ) + \
                                  "<A href='http://thetvdb.com/?tab=episode&seriesid=%s&seasonid=%s&id=%s'>s%se%s</A><BR />\n" % (tvdbid, seasonid, id, SeasonNumber, EpisodeNumber) + Overview
          if absolute_number=="a" and not absolute_number=="":                                 #   If absolute numbering and absolute episod number present
            tvdbSummary [ "s1e%s" + absolute_number                ] = Overview                #     In tvdbSummary Add at key s1ex the Overview (summary)
          else:                                                                                #   Otherwise (only season 1 have absolute nb)
            tvdbSummary [ "s%se%s" % (SeasonNumber, EpisodeNumber) ] = Overview                #     In tvdbSummary Add at key sxey the Overview (summary)
      Log.Debug("parseAniDBXml - Episode Summaries - " + str(tvdbSummary.keys))
        
    ### Collections ###
    #
    # AniDB.net telated anime tag in the serie XML
    # --------------------------------------------
    # <relatedanime>
    #   <relatedanime>
    #     <anime id="4"    type="Sequel" >Seikai no Senki               </anime>
    #     <anime id="6"    type="Prequel">Seikai no Danshou             </anime>
    #     <anime id="1623" type="Summary">Seikai no Monshou Tokubetsuhen</anime>
    #</relatedanime>
    #
    # Anime type: Same Setting, Alternative Setting, Sequel, Prequel, Side Story, Other
    #
    metadata.collections.clear()
    if movie:
      self.anidbCollectionMapping(metadata, metadata.id)                                     # Group movies into collections, using anime-movieset-list.xml
    relatedSeriesRoot = {'205':'Tenchi Muyou!'}
    if metadata.id in relatedSeriesRoot:
      metadata.collections.add(relatedSeriesRoot[metadata.id])
    for relatedAnime in anime.xpath('/anime/relatedanime/anime'):
      relatedAnimeID    = relatedAnime.get('id')
      relatedAnimeType  = relatedAnime.get('type')
      relatedAnimeTitle = relatedAnime.text
      if metadata.id in relatedSeriesRoot:
        metadata.collections.add(relatedSeriesRoot[metadata.id])
        break
    
    ### Studio ###
    # Studio pic - XBOX: .png file, white-on-clear, sized 161px x 109px, Save it in 'skin.aeon.nox"/media/flags/studios/'
    #                               Already created ones: https://github.com/BigNoid/Aeon-Nox/tree/master/media/flags/studios
    #              Plex: 512x288px .png located in 'Plex/Library/Application Support/Plex Media Server/Plug-ins/Media-Flags.bundle/Contents/Resources/'
    if not studio == "" and metadata.studio == "":                                           # Need to be after "elf.anidbTvdbMapping(metadata)"
      metadata.studio = studio

    ### Creator data  Aside from the animation studio, none of this maps to Series entries, so save it for episodes ###
    if movie:
      metadata.writers.clear()                                                               # Empty list of writers
      metadata.producers.clear()                                                             # Empty list of producers
      metadata.directors.clear()                                                             # Empty list of Directors
      ### tagline ###
      ### duration ###
      ### Countries ###
    
    else:
      writers   = []
      directors = []
      producers = []
    temp = ""
    for creator in anime.xpath('creators/name'):
      nameType = creator.get('type')
      
      if nameType == "Animation Work":                                                        # Studio
        if metadata.studio == "":                                                             # if not filled by AniDB to TVDB mapping file
          metadata.studio = creator.text;                                                     #   Set studio in metadata
        temp           += "Studio: %s, " % creator.text
        
      if "Direction" in nameType:                                                             # Direction, Animation Direction, Chief Animation Direction, Chief Direction
        if movie:                                                                             # if movie
          metadata.directors.add(director)                                                    #   Add director
        else:                                                                                 # else it's a serie
          directors.append(creator.text)                                                      #   add to directors[] for episodes
        temp += "%s is director, " % creator.text
        
      if nameType == "Series Composition":                                                    # Series Composition is basically a producer role 
        if movie:                                                                             # if movie
          metadata.producers.add(producer)                                                    #   Add Producer
        else:                                                                                 # else it's a serie
          producers.append(creator.text)                                                      #   Add to producers[] for episodes
        temp += "%s is producer, " % creator.text
        
      if nameType == "Original Work" or "Script" in nameType or "Screenplay" in nameType:     # Original mangaka => 'writers' is the best we can map to / Script writer
        if movie:                                                                             # if movie
          metadata.writers.add(writer)                                                        #   Add movie writer
        else:                                                                                 # else it's a serie
          writers.append(creator.text)                                                        #   Add to writers[] for episodes
        temp += "%s is writer, " % creator.text
    
    Log.Debug("parseAniDBXml - Categories - Creator data: " + temp)

    if not movie: ### TV Serie specific #################################################################################################################
      numEpisodes   = 0
      totalDuration = 0;
      for episode in anime.xpath('episodes/episode'):   ### Episode Specific ###########################################################################################
        #absolute_index 
        eid       = episode.get('id')
        epNum     = episode.xpath('epno')[0]
        epNumType = epNum.get('type')
        season    = ("0" if epNumType == "2" else "1" if epNumType == "1" else "")           # Normal episode
        epNumVal  = ( epNum.text[1:] if epNumType == "2" and epNumVal[0] == ['S'] else epNum.text )
        if epNumVal[0] in ['C', 'T', 'P', 'O']:                                              # Specials are prefixed with S(Specials 000-100), C(OPs, EDs 101-199),
            continue                                                                         #       T(Trailers 201-299), P(Parodies 301-399), O(Other    401-499)
           
        if not (season in media.seasons and epNumVal in media.seasons[season].episodes):     #Log missing episodes
          Log("parseAniDBXml - You are missing: " + metadata.title + " s" + season + "e" + epNumVal )
          continue
          
        episodeObj = metadata.seasons[season].episodes[epNumVal]                             # easier to manipulate, as it's going to be used a lot below

        ### Writers, etc... ###
        episodeObj.writers.clear()                                                           #
        for writer in writers:                                                               #
          episodeObj.writers.add(writer)                                                     #
          
        episodeObj.producers.clear()                                                         #
        for producer in producers:                                                           #
          episodeObj.producers.add(producer)                                                 #
        
        episodeObj.directors.clear()                                                         #
        for director in directors:                                                           #
          episodeObj.directors.add(director)                                                 #
          
        try:
          rating = getElementText(episode, 'rating')                                         # Get rating if present
          if rating != "":                                                                   # If rating not empty
            episodeObj.rating = float(rating)                                                #   Update rating
        except:
          pass                                                                               # Consinue, as rating is optional
      
        ### turn the YYYY-MM-DD airdate in each episode into a Date ###
        airdate = getElementText(episode, 'airdate')
        if airdate != "":
          match = re.match("([1-2][0-9]{3})-([0-1][0-9])-([0-3][0-9])", airdate)
          if match:
            try:
              episodeObj.originally_available_at = datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            except ValueError, e:
              Log.Debug("parseAniDBXml - parseAirDate - Date out of range: " + str(e))
              pass
            
        ### Get the correct episode title ###
        episodeObj.title, temp = self.getMainTitle (episode.xpath('title'), EPISODE_LANGUAGE_PRIORITY)
        if episodeObj.title=="" :                                                            # if no title
          episodeObj.title = epNum.text                                                      #   use epNum.text as for specials it's still prefixed with S  
        
        ### TVDB mapping episode summary ###
        temp = "parseAniDBXml - Episode Summaries - AniDB->TVDB mapped: "
        if not movie and not restrictedContent:                                              # TVDB doesn't index movies, nor 18+ anime
          anidb_ep = 's' + season + 'e' + epNumVal                                           # Set anidb_ep episode number
          if not tvdbid in ['movie', 'OAV', 'hentai', 'unknown', 'tv special', None]:        # If tvdb id not invalid ( it is a TV Serie)
            if anidb_ep in mappingList and mappingList[anidb_ep] in tvdbSummary :            #   If ep in mapping list and mapped ep in the summary list
              tvdb_ep = mappingList [ anidb_ep ]                                             #     tvdb_ep correcponding episode is through the mapping list
            elif defaulttvdbseason=="a" and anidb_ep in tvdbSummary:                         #   else if tvdb have absolute listing and ep in summary list
              tvdb_ep = anidb_ep                                                             #     tvdb_ep in absolute numbering is the anidb id
            elif "s"+defaulttvdbseason+"e"+epNumVal in tvdbSummary:                          #   else mapped season ep exist (implies: and not defaulttvdbseason=="a")
              tvdb_ep = "s"+defaulttvdbseason+"e"+epNumVal                                   #     tvdb_ep used the mapped default season
            if not tvdb_ep == None:                                                          #   if tvdb_ep variable defines
              summary = ( tvdbSummary [ tvdb_ep ] if not tvdb_ep == None else "" )           #     update summary with tvdbSummary at 'tvdb_ep' key
              summary = "AniDB.net: <A href='http://anidb.net/perl-bin/animedb.pl?show=anime&aid=%s'>%s</A> > "          % (metadata.id, metadata.title) + \
                                   "<A href='http://anidb.net/perl-bin/animedb.pl?show=ep&eid=%s'   >s%se%s</A><BR />\n" % (eid, season, epNumVal) + summary # update summary with tvdbSummary at 'tvdb_ep' key
              episodeObj.summary = summary                                                     #     update summary with tvdbSummary at 'tvdb_ep' key
              if not tvdb_ep == anidb_ep:                                                   # Because if there is no mapping to be done, no point seeing the logs
                temp += "%s>%s, " % (anidb_ep, tvdb_ep)
            else:
              Log.Debug("parseAniDBXml - Episode Summaries - AniDB episod '"+anidb_ep+"' could not be mapped - defaulttvdbseason: " + defaulttvdbseason)
          Log.Debug(temp)
              
        ### Duration ###
        duration = getElementText(episode, 'length')
        if duration != "":                                                                   # If duration present
          episodeObj.duration = int(duration) * 1000 * 60                                    #   Save duration in millisecs, AniDB stores it in minutes
          if season == 1:                                                                    #    If it is a serie then
            numEpisodes   += 1                                                               #    One more episode for the average to come
            totalDuration += episodeObj.duration                                             #    Adding episode duration
          
      ### Final post-episode titles cleanup ###
      if numEpisodes: #if movie getting scrapped as episode number by scanner...
        metadata.duration = int(totalDuration) / int(numEpisodes)     

    Log.Debug('--- parseAniDBXml - end -------------------------------------------------------------------------------------------------')

  ### Pull down the XML (and cache it) for a given anime ID ############################################################################################################
  def urlLoadXml(self, url):
    Log('anidbLoadXml (%s)' % url)
    global lastRequestTime
    lastRequestTime = datetime.datetime.utcfromtimestamp(0);
    try:
      networkLock.acquire()
      tries = 2
      while tries:
        delta = datetime.datetime.utcnow() - lastRequestTime;
        if delta.seconds < SECONDS_BETWEEN_REQUESTS:                                         #On AniDB.net, requests closer than 2 secs apart will get you banned
          time.sleep(SECONDS_BETWEEN_REQUESTS - delta.seconds)
        result = None
        try:
          lastRequestTime = datetime.datetime.utcnow()
          result          = HTTP.Request(url, headers={'Accept-Encoding':''}, timeout=60)
        except Exception, e:
          Log("anidbLoadXml(" + url + ") - Error: " + e.code)
          return None;
        if result == "<error>Banned</error>":
          Log('urlLoadXml - You have been Banned by AniDB.net. more than a xml every 2s OR downloaded more than once the title database')
        if result != None:
          return XML.ElementFromString(result)
        tries -= 1
    finally:
      networkLock.release()
    return None;

  ### Get the tvdbId from the AnimeId #######################################################################################################################
  def anidbTvdbMapping(self, metadata ):
    
    # --------------------------------   -----------------   --------------------------------------------------------------------------------------------------------
    # ScudLee anime-list-full.xml Tags   attributes          Description
    # --------------------------------   -----------------   --------------------------------------------------------------------------------------------------------
    # anime-list 
    #   anime                            anidbid             AniDB.net   serie unique id
    #                                    tvdbid              TheTVDB.com serie unique id
    #                                    defaulttvdbseason   which season of TheTVDB.com the anidb eps maps to by default, overwritten by the mapping list
    #                                    imdbid              [optional] IMDB serie unique ID
    #                                    tmdbid              [optional] The Movie Database serie unique ID
    #     name                           [text]              Main Anime title                                      
    #     supplemental-info                                  [optional] contain only studio tag so far
    #       studio                       [text]              Animation studio, when absent from AniDB.net
    #     mapping-list                                       Contain mapping list when AniDB.net and TheTVDB.com episode numbers differs
    #       mapping                      anidbseason         AniDB.net season
    #                                    tvdbseason          TheTVDB.com season
    #                                    [text]              Episode mapping anidb_ep-tvdb_ep separated by ';', also present at the beginning & end of the string
    # --------------------------------   -----------------   --------------------------------------------------------------------------------------------------------
    
    anidbid     = metadata.id
    mappingList = {}
    tree = self.xmlElementFromFile(ANIDB_TVDB_MAPPING, ANIDB_TVDB_MAPPING_URL)               # Load XML file
    for anime in tree.iterchildren('anime'):                                                 # For anime in matches.xpath('/anime-list/anime')
      if anidbid == anime.get("anidbid"):                                                    # If it is the right anime id
        tvdbid            = anime.get('tvdbid')                                              #   Get tvdb id
        defaulttvdbseason = anime.get('defaulttvdbseason')                                   #   get default tvdb season
        #tmdbid           = anime.get('tmdbid')                                              #   TheMovieDatabase id
        #imdbid           = anime.get('imdbid')                                              #   IMDB id
        
        try:
          studio           = anime.xpath("supplemental-info/studio")[0].text                 # Try to get Anime studio if present 
        except:                                                                              # But if not there
          studio = ""                                                                        # Make the variable empty
          pass
          
        if tvdbid in ['movie', 'OAV', 'hentai', 'unknown', 'tv special', None]:              # If tvdb id not available
          if tvdbid =='unknown':                                                             #   If the xml mapping file possibly needs updating, log it
            Log("[anime-list-full.xml] Missing tvdbid for anidbid %s update on https://github.com/ScudLee/anime-lists/blob/master/anime-list-todo.xml" % metadata.id);
        else:                                                                                # Else if Anime id valid
          #try:
          #  before = anime.xpath("before")[0].text
          #except:
          #  before = ""
          #  pass
          try:
            for season in anime.iterchildren('mapping-list'):                                # For each season mapping line in mapping list
              for string in season.text.split(';'):                                          #   Split the sting between semi-colon
                if string=="":                                                               #   If empty
                  continue                                                                   #   Just skip it
                eps = string.split('-')                                                      #   Split it into AniDB and theTVDB episodes
                Log.Debug( 's' + season.get("anidbseason") + 'e' + eps[0] + ' = s'+ season.get("tvdbseason") + 'e' + eps[1])
                mappingList [ 's' + season.get("anidbseason") + 'e' + eps[0] ] = 's' + season.get("tvdbseason") + 'e' + eps[1]   #save mapping in the format s1e123
          except:                                                                            # But if failed
            mappingList = {}                                                                 # Leave it empty
            pass         
        Log("gettvdbId(%s) tvbdid: %s studio: %s defaullttvdbseason: %s" % (anidbid, tvdbid, studio, str(defaulttvdbseason)) )
        if metadata.studio == "":  
          metadata.studio = studio  
        return tvdbid, defaulttvdbseason, mappingList, studio

    Log.Debug('anidbTvdbMapping('+animeId+') found no corresponding tvdbId')
    return "", "",[], ""

  ### [banners.xml] Attempt to get the TVDB's image data ###############################################################################################################
  def getImagesFromTVDB(self, metadata, media, tvdbSeriesId):

    # ----------------------------------   -------   ------------   -------------------------------------------------------------------------------------------------------
    # theTVDB.com banners.xml Tags         Used by   Values         Description
    # ----------------------------------   -------   ------------   -------------------------------------------------------------------------------------------------------
    # Banners
    #   Banner
    #     id                               ALL                      TVDB serie ID
    #     BannerPath                       ALL       path           Can be appended to <mirrorpath>/banners/ to determine the actual location of the artwork.
    #     BannerType                       ALL       fanart         ...  
    #                                                poster         ...  
    #                                                series         ...  
    #                                                season         ...     
    #     BannerType2                      fanart    1280x720       ...
    #                                                1920x1080      ...
    #                                      poster    680x1000       ...
    #                                      series    blank          will leave the title and show logo off the banner
    #                                                text           will show the series name as plain text in an Arial font
    #                                                graphical      will show the series name in the show's official font or will display the actual logo for the show
    #                                      season    season         will be the same dimensions as standard DVD cover format
    #                                                seasonwide     will be the same dimensions as the series banners
    #     Colors                           fanart    Null/rx|gx|bx  These are colors the artist picked that go well with the image.
    #                                                               In order they are Light Accent Color, Dark Accent Color and Neutral Midtone Color. 
    #                                                               It's meant to be used if you want to write something over the image, it gives you a good idea of what colors may work and show up well.
    #     Language                         ALL       en, ...        Some banners list the series name in a foreign language. The language abbreviation will be listed here.
    #     Season                           ?         season         If the banner is for a specific season, that season number will be listed here.
    #     Rating                           ALL                      Returns either null or a decimal with four decimal places. The rating the banner currently has on the site.
    #     RatingCount                      ALL       unsigned int   Number of people who have rated the image.
    #     SeriesName                       fanart    Bolean         Indicates if the seriesname is included in the image or not.
    #     ThumbnailPath                    fanart    path           Path to the thumbnail pic, diplayed if fanart only
    #     VignettePath                     fanart    path           Used exactly the same way as BannerPath, only shows if BannerType is fanart.
    # ----------------------------------   -------   ------------   -------------------------------------------------------------------------------------------------------
    
    PreferAnidbPoster = Prefs['PreferAnidbPoster'];
    GetTvdbPosters    = Prefs['GetTvdbPosters'   ];
    GetTvdbFanart     = Prefs['GetTvdbFanart'    ];
    GetTvdbBanners    = Prefs['GetTvdbBanners'   ];
    bannersXml = XML.ElementFromURL( TVDB_BANNERS_URL % (TVDB_API_KEY, tvdbSeriesId), cacheTime=(CACHE_1HOUR * 720)) # don't bother with the full zip, all we need is the banners 
    Log('getImagesFromTVDB([METADATA],%s) GetTvdbPosters: %s, GetTvdbFanart: %s, GetTvdbBanners: %s, PreferAnidbPoster: %s' %(tvdbSeriesId, GetTvdbPosters, GetTvdbFanart, GetTvdbBanners, PreferAnidbPoster))
    num = 0
    for banner in bannersXml.xpath('Banner'):                                                 # For each picture reference in the banner file
      num += 1                                                                                # Increase their count
      if banner.xpath('Language')[0].text != 'en':                                            # Skipping non-english images as AniDB/theTVDB english mainly as is this metadata agent
        continue

      bannerType     = banner.xpath('BannerType'   )[0].text                                  #
      bannerType2    = banner.xpath('BannerType2'  )[0].text                                  #
      bannerPath     = banner.xpath('BannerPath'   )[0].text                                  #
      season         = banner.xpath('season'       )                                          # Season if it is a season poster
      if 0 in season:
        season = season[0].text
      else:
        season = ""  
      proxyFunc      = (Proxy.Preview if bannerType=='fanart' else Proxy.Media)               # Manage preview for if pic is a fanart
      bannerRealUrl  = TVDB_IMAGES_URL + bannerPath
      bannerThumbUrl = TVDB_IMAGES_URL + (banner.xpath('ThumbnailPath')[0].text if bannerType=='fanart' else bannerPath)
      metaType       = (metadata.art                     if bannerType=='fanart' else \
                        metadata.posters                 if bannerType=='poster' else \
                        metadata.banners                 if bannerType=='series' else \
                        metadata.seasons[season].posters if bannerType=='season' and bannerType2=='season' else None)
                          
      if GetTvdbFanart  and   bannerType == 'fanart' or \
         GetTvdbPosters and ( bannerType == 'poster' or bannerType2 == 'season' ) or \
         GetTvdbBanners and ( bannerType == 'series' ): 
        if not bannerRealUrl in [metadata.art, metadata.posters, metadata.banners, metadata.seasons[season].posters]: 
          try:
            metaType[bannerRealUrl] = proxyFunc(HTTP.Request(bannerThumbUrl).content, sort_order=(num + 1 if PreferAnidbPoster and GetTvdbPosters else num))
          except:
            Log.Debug('getImagesFromTVDB - error downloading banner url1: %s, url2: %s' % (bannerRealUrl, bannerThumbUrl))
            pass
         
  ### AniDB collection mapping #######################################################################################################################
  def anidbCollectionMapping(self, metadata, animeId ):
  
    # --------------------------------   ----------   -------------------------------------------------------------------------------------------------------
    # ScudLee anime-movieset-list Tags   Attributes   Description
    # --------------------------------   ----------   -------------------------------------------------------------------------------------------------------
    # anime-set-list
    #   anime                            anidbid      AniDB.net unique anime id
    #                                    [text]       Main title
    #   titles
    #     title                          type         main, official, syn, short
    #                                    xml:lang     AniDB.net language
    #                                    [text]
    
    tree = self.xmlElementFromFile(ANIDB_COLLECTION_MAPPING, ANIDB_COLLECTION_MAPPING_URL)
    try:
      element = tree.iterfind("anime[@anidbid='%s']" % animeId)[0]
    except:
      Log("anidbCollectionMapping([metadata], %s) - %s is not part of any collection" % (animeId, animeId.zfill(5)) )
      return
    collection , temp = self.getMainTitle( element.getparent().xpath('/titles/title'), SERIE_LANGUAGE_PRIORITY)
    metadata.collections.clear()
    metadata.collections.add(collection)
    Log.Debug('anidbCollectionMapping - animeId.zfill(5) is part of collection: %s' % (animeId, collection) )

### TV Agent declaration ###############################################################################################################################################
class HamaTVAgent(Agent.TV_Shows, HamaCommonAgent):
  name             = 'HamaTV'
  languages        = [ Locale.Language.English, ]
  accepts_from     = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.opensubtitles']
  primary_provider = True
  fallback_agent   = False
  contributes_to   = None
 
  def search(self, results, media, lang, manual):
    self.searchByName(results, lang, media.show, media.year)

  def update(self, metadata, media, lang, force):
    self.parseAniDBXml(metadata, media, force, False)

### Movie Agent declaration ############################################################################################################################################
class HamaMovieAgent(Agent.Movies, HamaCommonAgent):
  name             = 'Hama TV/Movies'
  languages        = [ Locale.Language.English, ]
  accepts_from     = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.opensubtitles']
  primary_provider = True
  fallback_agent   = False
  contributes_to   = None

  def search(self, results, media, lang, manual):
    self.searchByName(results, lang, media.name, media.year)
 
  def update(self, metadata, media, lang, force):
    self.parseAniDBXml(metadata, media, force, True)
