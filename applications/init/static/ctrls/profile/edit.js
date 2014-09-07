sharoticaApp.controller('profileedit', function($scope, $http, $rootScope, $timeout) {
/* START CTRL */

	if ($rootScope.rawData) {
		$scope.account = $rootScope.rawData.account;
		$scope.albums = $rootScope.rawData.albums;
		$scope.profileFormData = $rootScope.rawData.profile;
		$scope.profileData = $rootScope.rawData.profile.data;
	}
	$scope.sortBy = '-viewLevel';
	$scope.NewProfileData = '';
	if ($scope.profileData.gender) {
		$scope.displayGender = true;
	} else {
		$scope.displayGender = false;
	}
	$scope.accountGender = '';
	$scope.selectImage = '';
	$scope.selectImageModal = false;
	$scope.selectBackGroundModal = false;
	$scope.imgToAdd = false;
	$scope.pickProfileImg = function(album) {
		$scope.selectImage = album.media;
		$scope.selectImageModal = true;
	};
	$scope.pickBackGroundImg = function(album) {
		$scope.selectImage = album.media;
		$scope.selectBackGroundModal = true;
	};
	$scope.changeProfileImg = function() {
		$scope.profileFormData.profileImg = false;
	};
	$scope.changeBackGroundImg = function() {
		$scope.profileFormData.backgroundImg = false;
	};
	$scope.changedProfile = function() {
		$http({
			method: 'POST',
			url: '/init/api_shar/edit_profile.json',
			data: $scope.profileFormData
		}).success(function(data) {
			$scope.account = data.account;
			$scope.albums = data.albums;
			$scope.profileFormData = data.profile;
			$scope.profileData = data.profile.data;
			document.getElementById('frame').src = document.getElementById('frame').src;
		});

	}
	$scope.addProfileData = function(flag) {
		var dataKey;
		var dataValue;
		if (flag == 'gender' && $scope.displayGender == false) {
			datakey = 'gender';
			dataValue = $scope.profileData.gender;
			addDataToProfile(dataKey, dataValue);
		} else if (flag == 'gender' && $scope.displayGender == true) {
			datakey = 'gender';
			dataValue = $scope.profileData.gender;
			removeDataFromProfile(dataKey, dataValue);
		} else if (flag == 'accountGender') {
			datakey = 'accountGender';
			dataValue = $scope.accountGender;
			addDataToProfile(dataKey, dataValue);
		}
	};
	$scope.updateProfileImage = function (image) {
		var dataKey;
		var dataValue;
		dataKey = 'newProfileImage';
		dataValue = image.thumbnail;
		addDataToProfile(dataKey, dataValue);
	};
	$scope.updateBackGroundImage = function (image) {
		var dataKey;
		var dataValue;
		dataKey = 'newBackGroundImage';
		dataValue = image.ID;
		addDataToProfile(dataKey, dataValue);
	};
	$scope.viewProfile = function () {
		window.location = "/init/profile/index";
	};
	
	function addDataToProfile(dataKey, dataValue) {
		$http({
			method: 'GET',
			url: '/init/api_shar/update_profile.json?key=' + dataKey + '&value=' + dataValue
		}).success(function(data) {
			$scope.account = data.account;
			$scope.albums = data.albums;
			$scope.profileFormData = data.profile;
			$scope.profileData = data.profile.data;
			if ($scope.profileData.gender) {
				$scope.displayGender = true;
			} else {
				$scope.displayGender = false;
			}
			$scope.accountGender = '';
			$scope.selectImage = '';
			$scope.selectImageModal = false;
			$scope.imgToAdd = false;
			$scope.selectBackGroundModal = false;
			document.getElementById('frame').src = document.getElementById('frame').src;
		});
	}
	function removeDataFromProfile(dataKey, dataValue) {
		$http({
			method: 'GET',
			url: '/init/api_shar/downdate_profile.json?key=' + dataKey + '&value=' + dataValue
		}).success(function(data) {
			$scope.album = data.album;
			$scope.mediaFormData = '';
			$scope.editImageModal = false;
		});
	}


/* END CTRL */
});