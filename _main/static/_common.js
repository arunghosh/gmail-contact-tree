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

        updateZoneSetting : function(z1, z2){
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

app.controller('userCtrl', function($scope, $rootScope, api){

    $rootScope.setBusy = function(msg){
        $rootScope.showBusy = true;
        $rootScope.busyText = msg;
    };

    $scope.updateMobile = function(){
        api.updateMobile($scope.user.phone).success(function(result){
            $scope.mobileEdit = false;
        });
    };

    api.userInfo().success(function(result){
        $scope.user = result;
    })

    $rootScope.treeView = false;
    $rootScope.contact = null;

    $rootScope.setContact = function(contact){
        $rootScope.contact = contact;
    };

    api.contacts().success(function(result){
        $rootScope.allContacts = result;
    });

    $rootScope.$watch("allContacts", function(newContacts, oldContacts)
    {
        if(newContacts) {
            onAllContactsUpdate();
        }
    });

    $rootScope.onContactUpdate = function(){
        onAllContactsUpdate();
    };

    function onAllContactsUpdate(){
        function updateCtrgys()
        {
            // $scope.contacts = $scope.allContacts.slice();
            var ctgrys = $scope.allContacts.map(function(c){
                return c.category;
            });
            ctgrys.sort();
            $rootScope.ctgrys = ctgrys.reduce(function(a,b){
                if(a.indexOf(b) < 0) a.push(b);
                return a;
            },[]);
            $rootScope.masterCtgrys = $rootScope.ctgrys.slice();
            $rootScope.onCtgryChange();        
        }

        function updateTreeView(){
            var temp = {'name':'contacts', 'children':[]};
            for(var i = 0; i < $rootScope.ctgrys.length; i++){
                var item = {'name':$rootScope.ctgrys[i], 'children':[]}
                var contacts = $rootScope.allContacts.reduce(function(a,b){
                    if($rootScope.ctgrys[i] === b.category) a.push(b);
                    return a;
                }, [])
                var mgnr = new ContactMgr();
                var zones = mgnr.zones;
                for(var j = 0; j < contacts.length; j++){
                    var contact = contacts[j];
                    var zone = zones[mgnr.getZone(contact)];
                    var cItem = {'name':contact.delta + " - " + contact.name,'color':zone.color};
                    zone.contacts.push(cItem);
                }
                for(var c = 0;c < 4; c++){
                    var zone = zones[c];
                    item.children.push({
                        'name': zone.name + ' #' + zone.contacts.length, 
                        'children':zone.contacts,
                        'color':zone.color});
                }
                temp.children.push(item);
            }
            treeView.showTree(temp);
        }

        updateCtrgys();
        updateTreeView();
    }
});

var Zone = function(id, name, color, show){
    this.id = id;
    this.name = name;
    this.color = color;
    this.nextStatus = name === "removed" ? 10 : 20;
    this.show = show;
    this.contacts = [];
};

var ContactMgr = function(){
    this.impIndex = 5;
    this.zones = [
                new Zone(0,'safe','#5c5', true),
                new Zone(1,'inter','#d84', true), 
                new Zone(2,'danger','#d33', true),
                new Zone(3,'removed','#888', false)];

    this.updateContacts = function(contacts){
        this.contacts = contacts;
        this.refreh();
    };

    this.getZone = function(contact){
        return contact.status == 20 ? 3 : contact.zone;
    }

    this.refreh = function(){
        var contacts = this.contacts;
        for(var i = 0; i < this.zones.length; i++) this.zones[i].contacts = [];
        for(var c = 0; c < contacts.length; c++){
            var contact = contacts[c];
            this.zones[this.getZone(contact)].contacts.push(contact)
        }
    };        
};

app.controller('zoneCtrl', function($scope, api, $rootScope){
    $scope.contacts = [];
    $scope.manager = new ContactMgr();
    $scope.seleCtgry = null;

    api.zones().success(function(result){
        $scope.zone1 = result.p1;
        $scope.zone2 = result.p2;
    });

    $scope.toggleCtgry = function(ctgry){
        if($rootScope.ctgrys.contains(ctgry)){
            $rootScope.ctgrys.remove(ctgry);
        } else{
            $rootScope.ctgrys.push(ctgry);
        }
        $rootScope.ctgrys.sort();
    };

    $scope.updateSettings = function(){
        $rootScope.setBusy("updating settings...");
        api.updateZoneSetting($scope.zone1, $scope.zone2).success(function(){
            window.location = "/";
        });
    };

    $rootScope.onCtgryChange = function(){
        $scope.seleCtgry = $scope.seleCtgry ? $scope.seleCtgry : $rootScope.ctgrys[0];
        if($scope.seleCtgry === "*"){
            $scope.contacts = $rootScope.allContacts.reduce(function(a,b){
                if(b.status == $scope.manager.impIndex) a.push(b);
                return a;
            }, [])

        } else {
            $scope.contacts = $rootScope.allContacts.reduce(function(a,b){
                if($scope.seleCtgry === b.category) a.push(b);
                return a;
            }, [])
        }
        if(!$rootScope.contact)$rootScope.contact = $scope.contacts[0];
        fillZoneContacts();
    };

    function fillZoneContacts(){
        $scope.manager.updateContacts($scope.contacts);
        $scope.zones = $scope.manager.zones;    
    }

    $scope.updateFollow = function(contact, status){
        api.updateStatus(contact.id, status).success(function(result){
            contact.status = status;
            fillZoneContacts();
        });
    };

    $scope.selectCtrgy = function(ctgry){
        $scope.seleCtgry = ctgry;
        $rootScope.onCtgryChange();
    };
});


app.controller('inboxCtrl', function($scope, api, $rootScope){

    $scope.busyMsg = null;

    $scope.refreshInbox = function(){
        $scope.busyMsg = "Fetching latest mails....";
        api.refreshInbox().success(function(result){
            onImport(result);
        }).error(function(){
            if(showBusy){
                onAccessFail();
            }
        });
    };

    $scope.importInbox = function(){
        $scope.busyMsg = "Importing Old Mails....";
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
        $scope.busyMsg = null;
    }

    function getRecentMails(){
        api.recentMails().success(function(result){
            addMailsUrl(result);
            $scope.mails = result;
        });
    }

    function addMailsUrl(mails){
        for(var i = 0; i < mails.length; i++){
            mails[i].url = "https://mail.google.com/mail/u/0/#inbox/" + mails[i].message_id;
        }
    }

    getRecentMails();
    $scope.refreshInbox();
});


app.controller('contactCtrl', function($scope, api, $rootScope){
    // $scope.$emit("abcd");
    function init()
    {
        $scope.showBusy = false;
    }   

    $scope.merge = function(dupeContact){
        var seleContact = $rootScope.contact;
        api.merege(seleContact, dupeContact).success(function(result){
            var allContacts = $rootScope.allContacts.slice();
            allContacts.remove(seleContact);
            allContacts.remove(dupeContact);
            allContacts.push(result);
            $rootScope.allContacts = allContacts;
            $rootScope.contact = result;
            dupeContact.email = "";
            dupeContact.isMerged = true;
        });
    };

    $scope.updateCtrgy = function(ctgry){
        api.updateCtrgy($rootScope.contact.id, ctgry).success(function(){
            $rootScope.contact.category = ctgry;
            $rootScope.ctgryEdit = false;
            $rootScope.onContactUpdate();
        });
    };


    $scope.$watch("dupeName", function(name, oldName){
        if(name){
            name = name.toLowerCase();
            $scope.duplicates = $rootScope.allContacts.reduce(function(a,b){
                if(~b.name.toLowerCase().indexOf(name) && $rootScope.contact.email != b.email) a.push(b);
                return a;
            },[]);
        }
    });

    $rootScope.$watch("contact", function(contact, oldContact){
        if(!contact) return;
        api.lnDuplicates(contact.id).success(function(result){
            $scope.lnDupes = result;
        }); 

        refreshCommItems();

        api.duplicates(contact).success(function(result){
            $scope.duplicates = result
        });
    });

    function refreshCommItems(){
          api.commItems($rootScope.contact).success(function(result){
            formatCommItems(result);
            $scope.commItems = result;
        });      
    }

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