# first line: 73
    @staticmethod
    def geocode(address: str):
        logging.info("Fetching geolocation for [{}] from LocationIQ".format(address))
        logging.info("Waiting 1 second to avoid rate limiting from LocationIQ")
        time.sleep(1)
        g = geocoder.locationiq(address, key=os.getenv('LOCATIONIQ_API_KEY'))
        return GeoLocation(g.latlng[0], g.latlng[1])
