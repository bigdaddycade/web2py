sharoticaApp.controller('dashboardalbum', function($scope, $http, $rootScope, $timeout) {
/* START CTRL 
	*/

	if ($rootScope.rawData) {
		$scope.album = $rootScope.rawData.album;
	}
	$scope.editImageModal = false;
	$scope.deleteAlbumModal = false;
	$scope.editAlbum = false;
	$scope.showBigImage = false;
	var modalIndex;
	$scope.launchModal = function(mediaIndex) {
		$scope.mediaFormData = $scope.album.media[mediaIndex];
		$scope.editImageModal = true;
		modalIndex = mediaIndex;
	};
	$scope.changeImage = function(flag) {
		if (flag == 'back') {
			if (modalIndex == 0) {
				modalIndex = $scope.album.media.length - 1;
				$scope.launchModal(modalIndex);
			} else {
				modalIndex = modalIndex - 1;
				$scope.launchModal(modalIndex);
			}
		} else if (flag == 'next') {
			if (modalIndex == $scope.album.media.length - 1) {
				modalIndex = 0;
				$scope.launchModal(modalIndex);
			} else {
				modalIndex++;
				$scope.launchModal(modalIndex);
			}
		}
	};
	$scope.closeModal = function(modal) {
		if (modal == 'edit') {
			$scope.mediaFormData = '';
			$scope.editImageModal = false;
		}else if (modal == 'delete') {
			$scope.deleteAlbumModal = false;
		}
	};
	$scope.removeImage = function() {
		$http({
			method: 'GET',
			url: '/init/api_shar/remove_media.json?media_id='
			+ $scope.mediaFormData.mediaId
			+ '&album_id='
			+ $scope.album.albumId
		}).success(function(data) {
			$scope.album = data.album;
			$scope.mediaFormData = '';
			$scope.editImageModal = false;
		});
	};
	$scope.deleteAlbum = function() {
		$scope.deleteAlbumModal = true;
	};
	$scope.setToEditAlbum = function(album) {
		if (album == 'nope') {
			$scope.albumEdit = false;
			$scope.albumFormData = '';
		} else {
			$scope.albumEdit = true;
			$scope.albumFormData = {};
			$scope.albumFormData.name = album.name;
			$scope.albumFormData.description = album.description;
			$scope.albumFormData.viewLevel = album.viewLevel;
			$scope.albumFormData.albumId = album.albumId;
			$scope.albumFormData.update = false;
		}
	};
	$scope.removeAlbum = function() {
		$http({
			method: 'GET',
			url: '/init/api_shar/remove_album.json?album_id='
			+ $scope.album.albumId
		}).success(function(data) {
			window.location = "/init/dashboard/index";
		});
	};
	$scope.editItem = function(itemType) {
		if (itemType == 'media') {
			$http({
				method: 'POST',
				url: '/init/api_shar/edit_media.json',
				data: $scope.mediaFormData
			}).success(function(data) {
				//do nothing
			});
		} else if (itemType == 'album') {
			$http({
				method: 'POST',
				url: '/init/api_shar/edit_album.json',
				data: $scope.albumFormData
			}).success(function(data) {
				$scope.album = data.album;
				$scope.albumEdit = false;
				$scope.albumFormData = '';
			});
		}
	};
	$scope.bigImageToggle = function(display) {
		if (display == 'show') {
			$scope.showBigImage = true;
		} else {
			$scope.showBigImage = false;
		}
	};

/* END CTRL */
});