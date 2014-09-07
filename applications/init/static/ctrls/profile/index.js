sharoticaApp.controller('profileindex', function($scope, $http, $rootScope) {
	/* JSON CALL
	
*/
	if ($rootScope.rawData) {
		$scope.albums = $rootScope.rawData.albums;
		$scope.profile = $rootScope.rawData.profile;
	}
	$scope.pageView = 'home';
	$scope.activeAlbum = '';
	$scope.mediaIndex = '';
	$scope.showBigImage = false;
	$scope.viewContent = function(view) {
		if (view == 'home') {
			$scope.pageView = 'home';
			$scope.activeAlbum = '';
		} else if (view == 'album') {
			$scope.pageView = 'album';
		} else if (view == 'editProfile') {
			window.location = "/init/profile/edit";
		} else if (view == 'back') {
			$scope.activeAlbum = '';
			if ($scope.pageView == 'media') {
				$scope.pageView = 'album';
			} else {
				$scope.pageView = 'home';
			}
		}
	};
	$scope.viewAlbum = function(album) {
		$scope.pageView = 'media';
		$scope.activeAlbum = album;
	};
	$scope.changeImage = function(flag) {
		if (flag == 'back') {
			if ($scope.mediaIndex == 0) {
				$scope.mediaIndex = $scope.activeAlbum.media.length - 1;
			} else {
				$scope.mediaIndex = $scope.mediaIndex - 1;
			}
		} else if (flag == 'next') {
			if ($scope.mediaIndex == $scope.activeAlbum.media.length - 1) {
				$scope.mediaIndex = 0;
			} else {
				$scope.mediaIndex++;
			}
		}
	};
	$scope.bigImageToggle = function(display, index) {
		if (display == 'show') {
			$scope.showBigImage = true;
			$scope.mediaIndex = index;
		} else {
			$scope.showBigImage = false;
			$scope.mediaIndex = '';
		}
	};
});