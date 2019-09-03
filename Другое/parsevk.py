import bs4

page = open('Аудиозаписи Юрия Ширкина _ 1312 аудиозаписей.html')
songsfile = open('songs', 'w')
artistsfile = open('artists_yuri', 'w')
soup = bs4.BeautifulSoup(page)

artists = {}
artists_list = []
songs = []

for name in soup.find_all('div', {'class': 'audio  fl_l'}):
    title_wrap = name.find('div', {'class': 'title_wrap fl_l'})
    artist = title_wrap.b.text

    try:
        title = title_wrap.find('span', {'class': 'title'}).text
    except AttributeError:
        title = title_wrap.find('span', {'class': 'title'}).text

    if artist in artists:
        artists[artist].append(title)
    else:
        artists[artist] = [title]

for artist in sorted(artists, key=lambda x: 1 / len(artists[x])):
    artists_list.append('{} - {}\n'.format(artist, len(artists[artist])))
    #~ for song in artists[artist]:
        #~ songs.append('{} - {}'.format(artist, song) + '\n')

artistsfile.writelines(artists_list)
#~ songsfile.writelines(songs)
