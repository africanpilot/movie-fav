from functools import cached_property
from typing import Optional
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

from link_domain.pyratebay.categories import categories
from link_lib.microservice_request import LinkRequest
from link_models.enums import ImportProviderTypeEnum


URL = "https://apibay.org/"

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding': 'none',
'Accept-Language': 'en-US,en;q=0.8',
'Connection': 'keep-alive'}

class Torrent(LinkRequest):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def __init__(self, id, name, info_hash, le, se, num_files, size, username, added, status, category, imdb=None):
		self.id = id
		self.url = 'https://thepiratebay.org/description.php?id='+id
		self.name = name
		self.info_hash = info_hash
		self.leechers = int(le)
		self.seeders = int(se)
		self.num_files = num_files
		self.size = size
		self.username = username
		self.added = added
		self.status = status
		self.category = category
		self.imdb = imdb
		self.description = None
  
	@cached_property
	def tracker_list(self):
		# self.redis_delete_keys_pipe(self.movie_redis_engine, [f"tracker_list"]).execute()
		trackers_loads = self.movie_redis_engine.get(f"tracker_list")
		if trackers_loads:
			trackers = json.loads(trackers_loads).get("trackers")
		else:
			trackers_url = "https://trackerslist.com/best.txt"
			soup = BeautifulSoup(requests.get(trackers_url, headers=HEADERS).content, "html.parser")
			trackers = soup.find_all(text=True)[0].split("\n\n")
			self.load_to_redis(self.movie_redis_engine, f"tracker_list", dict(trackers=trackers), ex=86400)
		return trackers

	def get_description(self):
		if self.description == None:
			r = requests.get(URL+'t.php', params={'id':self.id})
			try:
				tor = r.json()
				self.description = tor['descr']
			except Exception as e:
				self.log.info('Error: ', e)

	def magnet(self):
		if self.info_hash == "0000000000000000000000000000000000000000":
			return None
  
		magnet_url = f'magnet:?xt=urn:btih:{self.info_hash}&dn={self.name}'
		for ln in self.tracker_list:
			tr = quote_plus(ln)
			magnet_url += f"&tr={tr}"

		return magnet_url
		

	def __str__(self):
		return f'Name: {self.name}\nHash: {self.info_hash}\nURL: {self.url}'


class PyratebayLib(LinkRequest):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
	def search(self, keyword, cats=[]) -> Optional[list[Torrent]]:
		params = {
			'q':keyword,
			'cat':[]
		}
		for cat in cats:
			if cat in categories:
				params['cat'].append(str(categories[cat]['code']))
		params['cat'] = ','.join(params['cat'])

		r = requests.get(URL+'q.php', params=params)

		torrents = []
		try:
			for tor in r.json():
				torrent = Torrent(tor['id'], tor['name'], tor['info_hash'], tor['leechers'], tor['seeders'],
					tor['num_files'], tor['size'], tor['username'], tor['added'], tor['status'], tor['category'], tor['imdb'])
				torrents.append(torrent)
		except Exception as e:
			self.log.info('Error: ', e)
			return None

		return torrents

	def get_torrent(self, torrent_id) -> Optional[Torrent]:
		r = requests.get(URL+'t.php', params={'id':torrent_id})

		try:
			tor = r.json()
		except Exception as e:
			self.log.info('Error: ', e)
			return None

		torrent = Torrent(str(tor['id']), tor['name'], tor['info_hash'], tor['leechers'], tor['seeders'],
				tor['num_files'], tor['size'], tor['username'], tor['added'], tor['status'], tor['category'], tor['imdb'])
		torrent.description = tor['descr']
		return torrent

	def recent(self) -> Optional[list[Torrent]]:
		r = requests.get(URL+'precompiled/data_top100_recent.json')
		torrents = []
		try:
			for tor in r.json():
				torrent = Torrent(tor['id'], tor['name'], tor['info_hash'], tor['leechers'], tor['seeders'],
						tor['num_files'], tor['size'], tor['username'], tor['added'], tor['status'], tor['category'], tor['imdb'])
				torrents.append(torrent)
		except Exception as e:
			self.log.info('Error: ', e)
			return None

		return torrents

	def top100(self, category=None, subc=None) -> Optional[list[Torrent]]:
		if category is None:
			r = requests.get('https://apibay.org/precompiled/data_top100_all.json')
		else:
			if category not in categories:
				raise Exception(f"{category} is not a valid category!")
			cat_n = categories[category]['code']
			if subc is not None and subc not in categories[category]['subs']:
				raise Exception(f"{subc} is not a valid sub-category!")
			elif subc is not None:
				cat_n += categories[category]['subs'][subc]
			r = requests.get(URL+f'precompiled/data_top100_{cat_n}.json')
		torrents = []
		try:
			for tor in r.json():
				torrent = Torrent(str(tor['id']), tor['name'], tor['info_hash'], tor['leechers'], tor['seeders'],
						tor['num_files'], tor['size'], tor['username'], tor['added'], tor['status'], tor['category'], tor['imdb'])
				torrents.append(torrent)
		except Exception as e:
			self.log.info('Error: ', e)
			return None
		return torrents


	def get_magnet_url(self, title: str, download_type: str, season: int = None, episode: int = None) -> Optional[str]:
		try:
			name = f"{title} {download_type}".replace("'", "")
			torrents = self.search(name, cats=['video']) or []
			
			# order by seeders
			match_torrents: list[Torrent] = sorted(torrents, key=lambda x: x.seeders, reverse=True)
			
			# filter for the correct season
			if season:
				has_season = [
					torrent
					for torrent in match_torrents
					if f"S{season:02d}" in torrent.name
				]
				if has_season:
					match_torrents = has_season

			# filter for the correct episode
			if episode:
				has_episode = [
					torrent
					for torrent in match_torrents
					if f"S{season:02d}E{episode:02d}" in torrent.name
				]
				if has_episode:
					match_torrents = has_episode
			
			# check if torrent has a known provider
			has_provider = [
				torrent
				for torrent in match_torrents
				if any(x in torrent.name for x in ImportProviderTypeEnum.list())
			]
			if has_provider:
				match_torrents = has_provider
			
			# filter for best sound quality
			has_best_sound = [
				torrent
				for torrent in match_torrents
				if any(x in torrent.name for x in ["DDP5.1", "Atmos"])
			]
			if has_best_sound:
				match_torrents = has_best_sound
			
			if match_torrents:
				return match_torrents[0].magnet()
			
			return None
		except Exception as e:
			self.log.error(f"Error getting magnet url for {title} {download_type} - {e}")
			return None
