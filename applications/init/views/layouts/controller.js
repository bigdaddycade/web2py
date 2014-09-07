			sharoticaApp.controller('sharoticaCtrl',
				[        "$scope", "$http", "$timeout", "$location", "LocalStorage", "$rootScope", "sharoticaService",
				function ($scope,   $http,   $timeout,   $location,   LocalStorage,   $rootScope,   sharoticaService) {
			/* START CTRL */

				var postData = {};
				var sharoticaStorage = new LocalStorage("shar");
				$scope.innerCircleList = [];
				$scope.goodFriendsList = [];
				$scope.friendList = [];
				$scope.publicList = [];
				$scope.blockedList = [];
				setFriendsList();

				function setFriendsList () {
					angular.forEach($rootScope.basicData.friends, function(friend){
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
				
{{if request.controller == 'search' and request.function == 'index':}}
{{pass}}
				
{{if request.controller == 'messages' and request.function == 'index':}}
				if ($rootScope.messageKey) {
					sharoticaStorage.set($rootScope.accountKey + '_mail', null);
					showMessageView($rootScope.messageKey);
				}
				$scope.currentTime = new Date().getTime();
				$scope.inboxCount = 0;
				$scope.sentCount = 0;
				$scope.deleteCount = 0;
				$scope.dropDownDisplay = '';
				$scope.listPaneDisplay = 'start';
				{{if request.vars.flag:}}
				$scope.messageView = '{{=request.vars.flag}}';
				{{else:}}
				$scope.messageView = '';
				{{pass}}
				$scope.newMessageData = {};
				$scope.newMessageData.key = '';
				$scope.newMessageData.subject = '';
				$scope.newMessageData.body = '';
				$scope.messageList = '';
				$scope.currentMessage = '';
				$scope.currentAccount = '';
				{{if request.vars.account_key:}}
				createNewMessageByKey('{{=request.vars.account_key}}');
				{{pass}}
				$scope.showDropDown = function(dropDown) {
					if ($scope.dropDownDisplay == dropDown) {
						$scope.dropDownDisplay = '';
					} else {
						$scope.dropDownDisplay = dropDown;
					}
				};
				$scope.showListPane = function(listPane, friend) {
					$scope.listPaneDisplay = listPane;
					$scope.messageView = '';
					$scope.currentMessage = '';
					if (friend) {
						$scope.currentAccount = friend
						var key = friend.key
						getMessagesByKey(key);
					} else if (listPane != 'friend') {
						getMessagesByFolder(listPane);
					}
				};
				$scope.showmessageView = function(messageKey) {
					showMessageView(messageKey);
				};
				function showMessageView(messageKey) {
					$http({
						method: 'GET',
						url: '/init/messages/get_message.json?message_key=' + messageKey
					}).success(function(data) {
						rawData = angular.fromJson(data);
						$scope.currentMessage = rawData.message;
						$scope.currentMessage.date = Date.parse($scope.currentMessage.whenSent);
						$scope.messageView = 'read';
						markMessageAsRead(messageKey);
					});
				}
				$scope.deleteMessage = function(messageKey, flag) {
					var extra = '';
					if (flag) {
						extra = '&undo=true';
					}
					$http({
						method: 'GET',
						url: '/init/messages/delete_message.json?message_key=' + messageKey + extra
					}).success(function() {
						angular.forEach($scope.messageList, function(message, index){
							if (messageKey == message.key) {
								$scope.messageList.splice(index, 1);
							}
						});
					});
				};
				$scope.composeNewMessage = function(post) {
					if (post) {
						$scope.newMessageData.key = $scope.currentAccount.accountKey;
						sendMessage($scope.newMessageData);
					} else {
						$scope.messageView = 'new';
					}
				};
				function createNewMessageByKey(accountKey) {
					$http({
						method: 'GET',
						url: '/init/messages/get_basic.json?account_key=' + accountKey
					}).success(function(data) {
						rawData = angular.fromJson(data);
						$scope.currentAccount = rawData.basics;
						angular.forEach($scope.basicData.friends, function(friend){
							if (friend.key == $scope.currentAccount.accountKey) {
								getMessagesByKey($scope.currentAccount.accountKey);
							}
						});
					});
				}
				function getMessagesByKey(accountKey) {
					$http({
						method: 'GET',
						url: '/init/messages/get_key.json?account_key=' + accountKey
					}).success(function(data) {
						rawData = angular.fromJson(data);
						setTimeDelta(rawData.messages, "friend");
					});
				}
				function getMessagesByFolder(folder) {
					$http({
						method: 'GET',
						url: '/init/messages/get_folder.json?folder=' + folder
					}).success(function(data) {
						rawData = angular.fromJson(data);
						setTimeDelta(rawData.messages, folder);
					});
				}
				function sendMessage(postData) {
					$http({
						method: 'POST',
						url: '/init/messages/send_message.json',
						data: postData
					}).success(function() {
						$scope.newMessageData = {};
						$scope.messageView = '';
						getMessagesByFolder('sent')
					});
				}
				function markMessageAsRead(readKey) {
					angular.forEach($scope.messageList, function(message){
						if (readKey == message.key) {
							message.hasRead = true;
						}
					});
				}
				function setTimeDelta(rawData, type) {
					$scope.messageList = rawData;
					$scope.listPaneDisplay = type;
					if ($scope.messageView != 'new') {
						$scope.messageView = '';
					}
					$scope.currentMessage = '';
					$scope.currentTime = new Date().getTime();
					angular.forEach($scope.messageList, function(message){
						var tempDate = Date.parse(message.whenSent);
						var deltaTime = $scope.currentTime - tempDate;
						if (deltaTime <= 3600000) {
							message.time = (deltaTime / 60000).toFixed(0) + ' minutes ago'
						} else if (deltaTime <= 86400000) {
							message.time = (deltaTime / 3600000).toFixed(0) + ' hours ago'
						} else if (deltaTime <= 604800000) {
							message.time = (deltaTime / 86400000).toFixed(0) + ' days ago'
						} else if (deltaTime <= 2419200000) {
							message.time = (deltaTime / 604800000).toFixed(0) + ' weeks ago'
						} else {
							message.time = false
						}

					});
				}

{{pass}}
{{if request.controller == 'profile' and request.function == 'friends':}}
				$scope.profileFriendsList = {{=XML(response.json(friends))}};
{{pass}}
{{if (request.controller == 'profile' and request.function == 'albums') or (request.controller == 'dashboard' and request.function == 'media_advanced'):}}
				$scope.album = {{=XML(response.json(album))}};
				{{if not request.function == 'media_advanced':}}
				$scope.albumComments = {{=XML(response.json(comments))}};
				$scope.albumCommentData = {};
				$scope.albumCommentData.commentT = '';
				$scope.albumCommentData.mediaLink = '';
				$scope.mediaComments = '';
				$scope.mediaCommentData = {};
				$scope.mediaCommentData.commentT = '';
				$scope.mediaCommentData.mediaLink = '';
				{{pass}}
				$scope.showBigImage = false;
				$scope.showComments = false;
				$scope.mediaIndex = '';
				$scope.mediaFormData = '';
				$scope.postAlbumComment = function() {
					postData = {};
					postData.cType = 'album';
					postData.key = $scope.album.albumKey;
					postData.commentT = $scope.albumCommentData.commentT;
					postData.mediaLink = $scope.albumCommentData.mediaLink;
					postData.accountKey = $scope.account.key;
					$http({
						method: 'POST',
						url: '/init/api_shar/create_comment.json',
						data: postData
					}).success(function(data) {
						rawData = angular.fromJson(data);
						$scope.albumComments = rawData.comments;
						$scope.albumCommentData.commentT = '';
						$scope.albumCommentData.mediaLink = '';
					});
				};
				$scope.postMediaComment = function() {
					postData = {};
					postData.cType = 'media';
					postData.key = $scope.album.media[$scope.mediaIndex].mediaId;
					postData.commentT = $scope.mediaCommentData.commentT;
					postData.mediaLink = $scope.mediaCommentData.mediaLink;
					postData.accountKey = $scope.account.key;
					$http({
						method: 'POST',
						url: '/init/api_shar/create_comment.json',
						data: postData
					}).success(function(data) {
						rawData = angular.fromJson(data);
						$scope.mediaComments = rawData.comments;
						$scope.mediaCommentData.commentT = '';
						$scope.mediaCommentData.mediaLink = '';
					});
				};
				$scope.deleteComment = function(commentID, index, type){
					$http({
						method: 'GET',
						url: '/init/api_shar/delete_comment.json?comment_id=' + commentID
						+ '&account_key=' + $scope.account.key
					}).success(function(data) {
						if (type == 'album') {
							$scope.albumComments.splice(index, 1);
						} else if (type == 'media') {
							$scope.mediaComments.splice(index, 1);
						}
					});
				}
				$scope.changeImage = function(flag) {
					if (flag == 'back') {
						if ($scope.mediaIndex == 0) {
							$scope.mediaIndex = $scope.album.media.length - 1;
						} else {
							$scope.mediaIndex = $scope.mediaIndex - 1;
						}
					} else if (flag == 'next') {
						if ($scope.mediaIndex == $scope.album.media.length - 1) {
							$scope.mediaIndex = 0;
						} else {
							$scope.mediaIndex++;
						}
					}
					getComments();
				};
				$scope.bigImageToggle = function(display, index) {
					if (display == 'show') {
						$scope.showComments = false;
						$scope.showBigImage = true;
						$scope.mediaIndex = index;
					} else {
						$scope.showComments = false;
						$scope.showBigImage = false;
						$scope.mediaIndex = '';
					}
					getComments();
				};
				$scope.commentsModalToggle = function() {
					$scope.showBigImage = false;
					$scope.showComments = true
				};
				$scope.editImage = function (index) {
					$scope.mediaIndex = index;
					$scope.mediaFormData = $scope.album.media[index];
				};
				$scope.removeMedia = function () {
					$http({
						method: 'GET',
						url: '/init/api_shar/remove_media.json?media_id='
						+ $scope.mediaFormData.mediaId
						+ '&album_id='
						+ $scope.album.albumId
					}).success(function(data) {
						$scope.album = data.album;
						$scope.mediaFormData = '';
					});
				};
				$scope.likeThisMedia = function (likeType, mediaID) {
					sharoticaService.likeMedia(likeType, mediaID).then(function() {
						angular.forEach($scope.album.media, function(media){
							if (media.mediaId == mediaID) {
								if (likeType == 'like') {
									media.isLiked = true;
									media.likes ++;
								} else {
									media.isLiked = false;
									media.likes = media.likes - 1;
								}
							}
						});
					});
				};
				$scope.editMedia = function () {
					$http({
						method: 'POST',
						url: '/init/api_shar/edit_media.json',
						data: $scope.mediaFormData
					}).success(function(data) {
						window.location = "/init/dashboard/media_advanced?album_key=" + $scope.album.albumKey + "#" + $scope.mediaIndex;
					});
				};
				function getComments() {
					postData = {};
					postData.cType = 'media';
					postData.key = $scope.album.media[$scope.mediaIndex].mediaId;
					postData.accountKey = $scope.account.key;
					$http({
						method: 'POST',
						url: '/init/api_shar/fetch_comments.json',
						data: postData
					}).success(function(data) {
						rawData = angular.fromJson(data);
						$scope.mediaComments = rawData.comments;
					});
				}
{{pass}}
{{if request.controller == 'profile' and request.function != 'browse':}}
				$scope.account = {}
				$scope.account.key = "{{if request.vars.account_key:
											=request.vars.account_key
										else:
											='self'
										pass}}";
				$scope.account.friendLevel = {{=basicData['friend']}};
				$scope.isFriend = {{=isFriend}};
				$scope.iAmAFriend = "{{=iAmAFriend}}";
				$scope.showFriendUpdate = false;
				$scope.makeNewFriend = function(block) {
					postData = {};
					postData.accountKey = $scope.account.key;
					postData.viewLevel = $scope.account.friendLevel;
					$http({
						method: 'POST',
						url: '/init/api_shar/add_friend.json',
						data: postData
					}).success(function(data) {
						if (!block) {
							if ($scope.account.friendLevel == 9) {
								$scope.showFriendUpdate = false;
								$scope.isFriend = false;
							} else {
								$scope.showFriendUpdate = false;
								$scope.isFriend = $scope.account.friendLevel;
							}
						} else if (block == 'unblock') {
							window.location = "/init/profile/about?account_key=" + $scope.account.key;
						} else {
							window.location = "/init/profile/broken?account_key=" + $scope.account.key;
						}
					});
				};
				$scope.showUpdateMenu = function(toggle) {
					if (toggle == 'off') {
						$scope.showFriendUpdate = false;
					} else if (toggle == 'block') {
						$scope.showFriendUpdate = 'block';
					} else if (toggle == 'unblock') {
						$scope.showFriendUpdate = 'unblock';
					} else if (toggle == 'unfriend') {
						$scope.showFriendUpdate = 'unfriend';
					} else {
						$scope.showFriendUpdate = 'add';
					}
				};

{{pass}}
			/* END CTRL */
			}]);

