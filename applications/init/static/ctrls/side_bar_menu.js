sharoticaApp.controller('sideBarMenuCtrl',
	[        "$scope", "$http", "sharoticaService", "LocalStorage",
	function ($scope,   $http,   sharoticaService,   LocalStorage) {
/* START CTRL */

	var sharoticaStorage = new LocalStorage("shar");
	$scope.innerCircleList = [];
	$scope.goodFriendsList = [];
	$scope.friendList = [];
	$scope.publicList = [];
	$scope.blockedList = [];
	$scope.basicData = '';
	$scope.unReadMessageCount = '';
	getBasicData();

	function getBasicData() {
		var tempHolder = sharoticaStorage.getObject('currentUser');
		if (tempHolder) {
			$scope.basicData = tempHolder;
		} else {
			sharoticaService.getBasicData(function(data) {
		        $scope.basicData = data;
		        sharoticaStorage.set("currentUser", data);
		        setFriendsList(data.friends);
		    });
		}
	}
	function setFriendsList (friendData) {
		angular.forEach(friendData, function(friend){
			if (friend.viewLevel == 2){
				$scope.innerCircleList.push(friend);
			} else if (friend.viewLevel == 3){
				$scope.goodFriendsList.push(friend);
			} else if (friend.viewLevel == 4){
				$scope.friendList.push(friend);
			} else if (friend.viewLevel == 5){
				$scope.publicList.push(friend);
			} else if (friend.viewLevel == 6){
				$scope.blockedList.push(friend);
			}
		});
	}
/* END CTRL */
}]);

