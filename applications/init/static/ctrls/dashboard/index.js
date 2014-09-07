sharoticaApp.controller('dashboardindex', function($scope, $http, $rootScope, $timeout) {
/* START CTRL 
	
	$http.get('http://local.sharotica.com/init/api_shar/account.json?user_id=superCade').success(function(data) {
		$scope.profile = data;
	});*/

	if ($rootScope.rawData) {
		$scope.albums = $rootScope.rawData.albums;
		$scope.profile = $rootScope.rawData.profile;
	}
	$scope.dataArray = "crazy";
	$scope.footerOff = true;
	$scope.blogView = false;
	$scope.commentView = false;
	$scope.mediaView = true;
	$scope.recentView = false;
	$scope.albumForm = false;
	$scope.albumFormData = {};
	$scope.albumFormData.viewLevel = $rootScope.rawData.defaults.album
	$scope.albumFormData.accountID = $rootScope.rawData.account

	$scope.addAlbum = function() {
		$scope.albumForm = true;
	}

	$scope.moveToMainView = function(view) {
		$scope.blogView = false;
		$scope.commentView = false;
		$scope.mediaView = false;
		$scope.recentView = false;
		if (view == 'blog') {
			$timeout(function() {$scope.blogView = true;},600);
		} else if (view == 'comment') {
			$timeout(function() {$scope.commentView = true;},600);
		} else if (view == 'media') {
			$timeout(function() {$scope.mediaView = true;},600);
		} else if (view == 'recent') {
			$timeout(function() {$scope.recentView = true;},600);
		}
		

	};
	$scope.createNewAlbum = function() {
		$http({
			method: 'POST',
			url: '/init/api_shar/create_album.json',
			data: $scope.albumFormData
		}).success(function(data) {
			$scope.albums = data.albums;
			$scope.albumForm = false;
		});
	};
	$scope.albumDetails = function(albumID) {
		window.location = "/init/dashboard/album?album_id=" + albumID;
	};
	$scope.getPage = function(pageView) {
		if (pageView == 'edit-account') {
			window.location = "/init/account/index";
		} else if (pageView == 'edit-profile') {
			window.location = "/init/profile/edit";
		} else if (pageView == 'view-profile') {
			window.location = "/init/profile/index";
		}
	};

/* END CTRL */
});