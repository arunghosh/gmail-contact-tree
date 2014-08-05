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


var app = angular.module('app', ['ngAnimate', 'angularCharts']);
app.config(function($interpolateProvider, $httpProvider) {
    // $interpolateProvider.startSymbol('{[');
    // $interpolateProvider.endSymbol(']}');
    $httpProvider.defaults.headers.post['X-CSRFToken'] = common.readCookie('csrftoken');
});



app.directive('slideable', function () {
    return {
        restrict:'C',
        compile: function (element, attr) {
            // wrap tag
            var contents = element.html();
            element.html('<div class="slideable_content" style="margin:0 !important; padding:0 !important" >' + contents + '</div>');

            return function postLink(scope, element, attrs) {
                // default properties
                attrs.duration = (!attrs.duration) ? '1s' : attrs.duration;
                attrs.easing = (!attrs.easing) ? 'ease-in-out' : attrs.easing;
                element.css({
                    'overflow': 'hidden',
                    'height': '0px',
                    'transitionProperty': 'height',
                    'transitionDuration': attrs.duration,
                    'transitionTimingFunction': attrs.easing
                });
            };
        }
    };
});

app.directive('slideToggle', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var target = document.querySelector(attrs.slideToggle);
            attrs.expanded = false;
            element.bind('click', function() {
                var content = target.querySelector('.slideable_content');
                if(!attrs.expanded) {
                    content.style.border = '1px solid rgba(0,0,0,0)';
                    var y = content.clientHeight;
                    content.style.border = 0;
                    target.style.height = y + 'px';
                } else {
                    target.style.height = '0px';
                }
                attrs.expanded = !attrs.expanded;
            });
        }
    }
});

app.directive('modalDialog', function() {
    return {
        restrict: 'E',
        scope: {show: '='},
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
        scope: {show: '='},
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
        var arr = input.split("T");
        return arr[0].replace(new Date().getFullYear(), "");
    };
});

app.filter("time", function() {
    return function(input) {
        var arr = input.split("T");
        return arr[1].substring(0,6);
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

        duplicates: function(contact){
            return $http.get("contact/duplicates/" + contact.id + "/");
        },

        commItems: function(contact){
            return $http.get("contact/comm_items/" + contact.id + "/");
        },

        commByMonth: function(contact){
            return $http.get("contact/by_month/" + contact.id + "/");
        },

        contacts : function(){
            return $http.get('contacts/');
        },

        merege : function(org, dup){
            return $http.post('contacts/merge/', {'org_id':org.id,'dup_id':dup.id});
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

Array.prototype.containsById = function(item){
    for(var i = 0; i < this.length; i++){
        if(this[i].id == item.id){
            return true;
        }
    }
    return false;   
};

Array.prototype.remove = function(item){
    var index = this.indexOf(item);
    this.splice(index,1);
};

app.controller('userCtrl', function($scope, api){
    $scope.updateMobile = function(){
        api.updateMobile($scope.user.phone).success(function(result){
            $scope.mobileEdit = false;
        });
    };

    api.userInfo().success(function(result){
        $scope.user = result;
    })
});

app.controller('zoneCtrl', function($scope, api, $rootScope){
    $scope.contacts = [];
    $scope.zones = ["Safe", "Inter", "Danger"];
    $scope.seleCtgry = 'personal';
    $rootScope.contact = null;

    api.zones().success(function(result){
        $scope.zone1 = result.p1;
        $scope.zone2 = result.p2;
    });

    $scope.updateZone = function(){
        api.updateZones($scope.zone1, $scope.zone2).success(function(){
            $scope.showZoneSet = false;
        });
    };

    $scope.setContact = function(contact){
        $rootScope.contact = contact;
    };

    refreshContacts();

    function refreshContacts(){
        api.contacts().success(function(result){
            $scope.contacts = result;
            $scope.masterContacts = result.slice();
            var ctgrys = result.map(function(c){
                return c.category;
            });
            $rootScope.ctgrys = ctgrys.reduce(function(a,b){
                if(a.indexOf(b) < 0) a.push(b);
                return a;
            },[]);
            $scope.onCtgryChange();
        });
    }

    $rootScope.onCtgryChange = function(){
        $scope.contacts = $scope.masterContacts.reduce(function(a,b){
            if($scope.seleCtgry === b.category) a.push(b);
            return a;
        }, [])
    }    

    $scope.updateStatus = function(contact, status){
        api.updateStatus(contact.id, status).success(function(result){
            contact.status = status;
        });
    };

    $scope.toggleCtrgy = function(ctgry){
        $scope.seleCtgry = ctgry;
        $rootScope.onCtgryChange();
    };
});

app.controller('contactCtrl', function($scope, api, $rootScope){
    // $scope.$emit("abcd");
    function init()
    {
        $scope.mails = [];
        $scope.showBusy = false;
        $scope.seleContacts = [];
        $scope.recentMails = [];
        getRecentMails();
        refreshInbox(false);
    }   

    $scope.merge = function(contact){
        api.merege($scope.contact, contact).success(function(){
            contact.status = true;
        });
    };

    $scope.updateCtrgy = function(ctgry){
        api.updateCtrgy($scope.contact.id, ctgry).success(function(){
            $scope.contact.category = ctgry;
            $scope.ctgryEdit = false;
            $rootScope.onCtgryChange();
        });
    };

    $scope.refreshInbox = function(){
        refreshInbox(true);
    }

    function refreshInbox(showBusy)
    {
        $rootScope.showBusy = showBusy;
        $rootScope.busyText = "Fetching latest mails....";
        api.refreshInbox().success(function(result){
            onImport(result);
        }).error(function(){
            if(showBusy){
                onAccessFail();
            }
        });
    };

    $scope.importInbox = function(){
        $rootScope.showBusy = true;
        $rootScope.busyText = "Importing Old Mails....";
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
            getRecentMails();
        }
        $rootScope.showBusy = false;
    }

    $rootScope.$watch("contact", function(contact, oldContact){
        if(!contact) return;
        $scope.recentMode = false;
        api.lnDuplicates(contact.id).success(function(result){
            $scope.lnDupes = result;
        }); 

        api.commItems(contact).success(function(result){
            formatCommItems(result);
            $scope.commItems = result;
        });

        api.duplicates(contact).success(function(result){
            $scope.duplicates = result
        });
    });


    function formatCommItems(items){
        for(var i = 0; i < items.length; i++){

            var item = items[i];
            item.dclass = item.direction == 1 ? item.dclass = "glyphicon-chevron-left" : "glyphicon-chevron-right";

            switch (item.type){
                case 2:
                    item.tclass = "glyphicon-comment";
                    break;
                case 3:
                    item.tclass = "glyphicon-earphone";
                    break;
                default:
                    item.tclass = "glyphicon-envelope";
            }

            if(item.mail_id){
                item.url = "https://mail.google.com/mail/u/0/#inbox/" + item.mail_id;
            }
        }
    }


    function addMailsUrl(mails){
        for(var i = 0; i < mails.length; i++){
            mails[i].url = "https://mail.google.com/mail/u/0/#inbox/" + mails[i].message_id;
        }
    }

    function getRecentMails(){
        api.recentMails().success(function(result){
            addMailsUrl(result);
            $scope.recentMails = result;
            $scope.recentMode = true;
        });
    }

    init();

});



app.controller("statCtrl", function($scope, $rootScope, $timeout, api) {
    $rootScope.$watch("contact", function(contact, oldContact){
        if(contact){
            api.commByMonth(contact).success(function(result){
                var data = []
                for(var i = 0; i < result.length; i++){
                    var item = {
                        x : result[i].month,
                        y : [result[i].mail_count, result[i].call_count],
                    };
                    data.push(item);
                }
                $timeout(function() {
                    $scope.data = {
                        title:'',
                        series: ['mails', 'calls'],
                        data : data,
                        tooltips:true,
                    };
                }, 100);
            });

            $scope.config = {
                title : contact.name,
                tooltips: true,
                labels: false,
                mouseover: function() {},
                mouseout: function() {},
                click: function() {},
                legend : {
                    display:true,
                    position:'left'
                },
                innerRadius: 0
            };

        }   
    });

    $scope.chartType = 'line';


});