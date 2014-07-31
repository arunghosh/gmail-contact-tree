var DATE_FORMAT = "DD, d M, yy";
var WEEK_DAYS = ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'];

var Day = function(slots, date){
    var way = date.getDay();
    this.slots = slots;
    this.date = date.toDateString();
    this.day = date.getDate();
    this.wday = WEEK_DAYS[way];
    this.class = (way == 0 || way == 6) ? 'hol' : '';
    this.details = false;
};

var Calender = function(){
    var date = new Date();
    this.months = ["Jan","Feb","Mar","Apr", "May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
    this.month = this.months[date.getMonth()];
    this.days = [];
    this.years = [];
    this.year = date.getFullYear();

    this.getMonthInt = function(){
        return this.months.indexOf(this.month) + 1;
    };

    this.getDateMDY = function(day){
        return this.year + "-" + this.getMonthInt() + "-" + day;
    };

    this.setSlots = function(dayMap){
        this.days = [];
        var date = new Date(this.year, this.getMonthInt(), 0);
        var max = date.getDate();
        for(var i = 1; i <= max; i++){
            var slots = dayMap[i] ? dayMap[i] : []; 
            date.setDate(i)
            var day = new Day(slots, date);
            this.days.push(day);
        }
    };

    this.addMonth = function(delta){
        var month = this.getMonthInt() + delta;
        if(month > 12){
            month = month - 12;
            this.year = year + 1;
        }
        if(month < 1){
            month = month + 12;
            this.year = year - 1;
        }
        this.month = this.months[month - 1];
    };

    for(var i = this.year - 1; i < this.year + 2; i++){
        this.years.push(i);
    }
};

var common = new function() {

    this.withCommas = function(x){
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    };

    this.readCookie = function(name){
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for(var i=0;i < ca.length;i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1,c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
        };
        return null;
    }
};


var app = angular.module('app', ['ngTouch']);
app.config(function($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    $httpProvider.defaults.headers.post['X-CSRFToken'] = common.readCookie('csrftoken');
});





app.directive('modalDialog', function() {
  return {
    restrict: 'E',
    scope: {
      show: '='
  },
    replace: true, // Replace with the template below
    transclude: true, // we want to insert custom content inside the directive
    link: function(scope, element, attrs) {
      scope.dialogStyle = {};
      scope.title = attrs.title;
      if (attrs.width) scope.dialogStyle.width = attrs.width;
      if (attrs.height) scope.dialogStyle.height = attrs.height;
      scope.hideModal = function() {
        scope.show = false;
    };
},
templateUrl: "/static/html/modal.html"
};
});

app.directive('busy', function() {
  return {
    restrict: 'E',
    scope: {
      show: '='
  },
    replace: true, // Replace with the template below
    transclude: true, // we want to insert custom content inside the directive
    link: function(scope, element, attrs) {
      scope.dialogStyle = {};
      scope.hideModal = function() {
        scope.show = false;
    };
},
templateUrl: "/static/html/busy.html"
};
});

app.filter("date_mdy", function() {
  return function(input) {
    var arr = input.replace("T","-").split("-");
    var date = new Date(arr[0], arr[1] - 1, arr[2]);
    return date.toDateString().substring(4,15);
};
});

app.factory('api', function($http){
    return {
        updateStatus: function(cid, status){
            return $http.post("contact/status/" + cid + "/" + status + "/");
        },

        updateCtrgy: function(cid, ctgry){
            return $http.post("contact/ctgry/" + cid + "/" + ctgry + "/");
        },

        contacts : function(){
            return $http.get('contacts/');
        },

        mails : function(cid){
            return $http.get('inbox/mails/'+ cid + "/");
        },

        refreshInbox : function(){
            return $http.get('inbox/refresh/');
        },

        importInbox : function(){
            return $http.get('inbox/import/');
        },

        recentMails : function(){
            return $http.get('inbox/recent/');
        },        

        calls : function(cid){
            return $http.get('mobile/calls/'+ cid + "/");
        },

        recentCalls : function(){
            return $http.get('mobile/recent/');
        },

        lnDuplicates : function(cid){
            return $http.get('lkdn/duplicates/'+ cid + "/");
        },

        zones : function(){
            return $http.get('setting/zones');
        },

        updateZones : function(z1, z2){
            return $http.post('setting/zones/', {'p1':z1,'p2':z2});
        },

        updateMobile : function(mobile){
            return $http.post('update_mobile/' + mobile + "/")
        },

        userInfo : function(){
            return $http.get('user_info')
        },
    };
});

Array.prototype.contains = function(item){
    for(var i = 0; i < this.length; i++){
        if(this[i] == item){
            return true;
        }
    }
    return false;   
};

Array.prototype.remove = function(item){
    var index = this.indexOf(item);
    this.splice(index,1);
};

app.controller('ctrl', function($scope, api){
    function init()
    {
        $scope.zones = ["Safe", "Inter", "Danger"];
        $scope.mails = [];
        $scope.showBusy = false;
        $scope.masterContacts = [];
        $scope.contacts = [];
        $scope.seleContacts = [];
        $scope.recentMails = [];
        $scope.seleCtgrys = ['personal', '--'];
        $scope.busyText = "Loading....";
        $scope.mobileEdit = false;
        refreshContacts();
        getRecentMails();
        refreshInbox(false);
        api.zones().success(function(result){
            $scope.zone1 = result.p1;
            $scope.zone2 = result.p2;
        });

        api.userInfo().success(function(result){
            $scope.user = result;
        })
    }   

    $scope.updateZone = function(){
        api.updateZones($scope.zone1, $scope.zone2).success(function(){

        });
    };

    $scope.updateCtrgy = function(ctgry){
        api.updateCtrgy($scope.contact.id, ctgry).success(function(){
            $scope.contact.category = ctgry;
            $scope.ctgryEdit = false;
            refreshContacts();
        });
    };

    $scope.updateMobile = function(){
        api.updateMobile($scope.user.phone).success(function(result){
            $scope.mobileEdit = false;
        });
    };

    function refreshContacts(){
        api.contacts().success(function(result){
            $scope.contacts = result;
            $scope.masterContacts = result.slice();
            var ctgrys = result.map(function(c){
                return c.category;
            });
            $scope.ctgrys = ctgrys.reduce(function(a,b){
                if(a.indexOf(b)<0) a.push(b);
                return a;
            },[]);
            onCtgrySelection();
        });
    }

    function onCtgrySelection(){
        $scope.contacts = $scope.masterContacts.reduce(function(a,b){
            if($scope.seleCtgrys.contains(b.category)) a.push(b);
            return a;
        }, [])
    }

    $scope.refreshInbox = function(){
        refreshInbox(true);
    }

    function refreshInbox(showBusy)
    {
        $scope.showBusy = showBusy;
        $scope.busyText = "Fetching latest mails....";
        api.refreshInbox().success(function(result){
            onImport(result);
        }).error(function(){
            if(showBusy){
                onAccessFail();
            }
        });
    };

    $scope.toggleCtrgy = function(ctgry){
        if($scope.seleCtgrys.contains(ctgry)){
            $scope.seleCtgrys.remove(ctgry)
        } else{
            $scope.seleCtgrys.push(ctgry);
        }
        onCtgrySelection();
    };

    $scope.importInbox = function(){
        $scope.showBusy = true;
        $scope.busyText = "Importing Old Mails....";
        api.importInbox().success(function(result){
            onImport(result);
        }).error(function(){
            onAccessFail();    
        });
    };


    function onAccessFail(){
        $scope.busyText = "Access Failed. Refreshing GMAIL Access Token....";
        window.location = "/gmail/";
    }

    function onImport(result){
        $scope.statusMsg = result.count + " mails imported";
        if(result.count > 0) {
            refreshContacts();
            getRecentMails();
        }
        $scope.showBusy = false;
    }

    $scope.updateStatus = function(contact, status){
        api.updateStatus(contact.id, status).success(function(result){
            contact.status = status;
        });
    };

    $scope.setContact = function(contact){
       
        $scope.contact = contact;
        if(!$scope.seleContacts.contains(contact)){
            $scope.seleContacts.push(contact);
        }

        api.lnDuplicates(contact.id).success(function(result){
            $scope.lnDupes = result;
        }); 

        api.mails(contact.id).success(function(result){
            setMails(result);
        });

        api.calls(contact.id).success(function(result){
            $scope.calls = result
        });

    };

    $scope.showRecent = function(){
        $scope.mails = $scope.recentMails;
        $scope.contact = null;
        $scope.lnDupes = [];
    };

    function setMails(mails){
        for(var i = 0; i < mails.length; i++){
            mails[i].url = "https://mail.google.com/mail/u/0/#inbox/" + mails[i].message_id;
        }
        $scope.mails = mails;
    }

    $scope.removeContact = function(contact){
        var contacts = $scope.seleContacts;
        contacts.remove(contact);
        if(contact == $scope.contact){
            if(contacts.length > 0){
                $scope.getMails(contacts[0]);
            } else{
                $scope.showMail = false;
            }
        }
    }

    function getRecentMails(){
        api.recentMails().success(function(result){
            if($scope.contact == null) setMails(result);
            $scope.recentMails = result;
        });
    }

    init();

});