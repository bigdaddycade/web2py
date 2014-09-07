sharoticaApp.factory("sharoticaService",
	[       "$q", "$http",  "$rootScope",
	function($q,   $http,    $rootScope) {

	return {
		createAlbum: function(uid, eventID) {
			return platformAPI.get("api_location/locations.json?uid=" + uid + "&event_id=" + eventID);
		},

		GetAlbums: function(uid, eventID, locID) {
			return platformAPI.get("api_location/checkin.json?uid=" + uid + "&event_id=" + eventID + "&loc_id=" + locID);
		}
	};

}]);
