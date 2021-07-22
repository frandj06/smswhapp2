/************************** IMPORTS **************************/

// import AOS from 'aos';
import anchorme from 'anchorme';
import 'core-js';
import 'regenerator-runtime/runtime';
import { MDCDialog } from '@material/dialog';
import { MDCDrawer } from "@material/drawer";
import { MDCFloatingLabel } from '@material/floating-label';
import { MDCIconButtonToggle } from '@material/icon-button';
import { MDCLinearProgress } from '@material/linear-progress';
import { MDCLineRipple } from '@material/line-ripple';
import { MDCList } from "@material/list";
import { MDCMenu, Corner } from '@material/menu';
import { MDCNotchedOutline } from '@material/notched-outline';
import { MDCRadio } from '@material/radio';
import { MDCRipple } from '@material/ripple';
import { MDCSelect } from '@material/select';
import { MDCSnackbar } from '@material/snackbar';
import { MDCTabBar } from '@material/tab-bar';
import { MDCTextField } from '@material/textfield';
import { MDCTextFieldHelperText } from '@material/textfield/helper-text';
import { MDCTextFieldIcon } from '@material/textfield/icon';
import { MDCTopAppBar } from '@material/top-app-bar';
import { Workbox } from 'workbox-window/Workbox.mjs';


/************************** FUNCTIONS **************************/

// Date getWeekOfMonth and getWeekOfYear implementation
Date.prototype.getDayString = function() {
    var weekdays = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
    return weekdays[this.getDay()];
};

Date.prototype.getWeekOfMonth = function(isMondayFirstDayOfWeek = true) {
    var d = new Date(this.getFullYear(), this.getMonth(), 1);
    var firstWeekday = d.getDay() - isMondayFirstDayOfWeek;
    if (firstWeekday < 0) firstWeekday = 6;
    var offsetDate = this.getDate() + firstWeekday - 1;
    return Math.floor(offsetDate / 7) + 1;
};

Date.prototype.getWeekOfYear = function() {
    var d = new Date(this.getFullYear(), this.getMonth(), this.getDate());
    var dayNum = d.getDay() || 7;
    d.setDate(d.getDate() + 4 - dayNum);
    var yearStart = new Date(d.getFullYear(),0,1);
    return Math.ceil((((d - yearStart) / 86400000) + 1)/7)
};

export function newDate(dt = new Date()) {
    return new Date(dt);
}
/* Allow 'window' context to reference the function */
window.newDate = newDate;


// Date Format
export function returnFormatDate(dateTime, type = '') {
    var dt = new Date(dateTime);
    var year = dt.getFullYear();
    var month = dt.getMonth() + 1; //months starts at 0
    var day = dt.getDate();
    var hours = dt.getHours();
    var min = dt.getMinutes();
    var sec = dt.getSeconds();

    var ampm = (hours >= 12) ? 'pm' : 'am';
    var hoursampm = ((hours + 11) % 12 + 1);

    if (month.toString().length == 1) {
        month = '0' + month;
    }
    if (day.toString().length == 1) {
        day = '0' + day;
    }
    if (hoursampm.toString().length == 1) {
        hoursampm = '0' + hoursampm;
    }
    if (min.toString().length == 1) {
        min = '0' + min;
    }
    if (sec.toString().length == 1) {
        sec = '0' + sec;
    }

    var returnDateTime = '';
    var formatDate = day + '/' + month + '/' + year;
    var formatTime = hoursampm + ':' + min + ' ' + ampm;
    if (type == 'full') {
        returnDateTime += formatDate + ' - ';
        returnDateTime += formatTime;
    } else if (type == 'date') {
        returnDateTime += formatDate;
    } else {
        returnDateTime += formatTime;
    }

    return returnDateTime;
}
/* Allow 'window' context to reference the function */
window.returnFormatDate = returnFormatDate;


// Fetch API
export function getFetch(url, actionFn = null, options = {}) {
    mdcTopBarLoading.open();
    return fetch(url, options)
        .then((response) => {
            if (response.status >= 200 && response.status < 300) {
                return Promise.resolve(response)
            } else {
                return Promise.reject(new Error(response.statusText))
            }
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('Request succeeded with JSON response: ', data);
            mdcTopBarLoading.close();
            if (actionFn) {
                let fn = (typeof actionFn == "string") ? window[actionFn] : actionFn;
                fn(data);
            }
            return Promise.resolve(data);
        })
        .catch(function (error) {
            console.log('Request failed: ', error);
            mdcTopBarLoading.close();
            return Promise.reject(error);
        });
}

export function postFetch(url, postData) {
    mdcTopBarLoading.open();
    return fetch(url, {
        method: 'POST',
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        credentials: 'include',
        body: JSON.stringify(postData)
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('Request succeeded with JSON response: ', data);
        mdcTopBarLoading.close();
        if ('cmd' in data && data.cmd == 'redirectURL') {
            window.location.assign(data.action);
        }
        return Promise.resolve(data);
    })
    .catch(function (error) {
        console.log('Request failed: ', error);
        mdcTopBarLoading.close();
        return Promise.reject(error);
    });
}


// Play/Stop Audio File
Audio.prototype.stop = function() {
    this.pause();
    this.currentTime = 0;
};

export function playAudio(audioEl, play) {
    if (play) {
        audioEl.play();
    } else {
        audioEl.stop();
    }
}


// Select Message Group
var msgGroup = null;
export function createMessageSelectList(elm, qty) {
    for (let index = 1; index <= qty; index++) {
        let listElm = document.createElement('li');
        let listTxt = document.createElement('span');

        listElm.classList.add('mdc-list-item');
        listElm.setAttribute('data-value', index);

        listTxt.classList.add('mdc-list-item__text');
        listTxt.textContent = 'Mensaje ' + index;

        listElm.appendChild(listTxt);
        elm.appendChild(listElm);
    }
}
export function selectMessageGroup(group) {
    let msgList = document.getElementById('selMessages').querySelector('ul');
    
    mdcAssignedVars['selMessages'].selectedIndex = -1;
    msgList.innerHTML = '';

    if (group == 'cg'){
        document.querySelector('.container-smswhapp-group--developer').classList.add('container--hidden');
        document.querySelector('.container-smswhapp-group--stakeholder').classList.add('container--hidden');
        document.querySelector('.container-smswhapp-group--treatment').classList.add('container--hidden');
        document.querySelector('.container-smswhapp-group--control').classList.remove('container--hidden');
        createMessageSelectList(msgList, 3);
    } else if (group == 'tg') {
        document.querySelector('.container-smswhapp-group--control').classList.add('container--hidden');
        document.querySelector('.container-smswhapp-group--developer').classList.add('container--hidden');
        document.querySelector('.container-smswhapp-group--stakeholder').classList.add('container--hidden');
        document.querySelector('.container-smswhapp-group--treatment').classList.remove('container--hidden');
        createMessageSelectList(msgList, 16);
    } else if (group == 'sg') {
        document.querySelector('.container-smswhapp-group--control').classList.add('container--hidden');
        document.querySelector('.container-smswhapp-group--developer').classList.add('container--hidden');
        document.querySelector('.container-smswhapp-group--treatment').classList.add('container--hidden');
        document.querySelector('.container-smswhapp-group--stakeholder').classList.remove('container--hidden');
        createMessageSelectList(msgList, 1);
    } else if (group == 'dg') {
        document.querySelector('.container-smswhapp-group--control').classList.add('container--hidden');
        document.querySelector('.container-smswhapp-group--stakeholder').classList.add('container--hidden');
        document.querySelector('.container-smswhapp-group--treatment').classList.add('container--hidden');
        document.querySelector('.container-smswhapp-group--developer').classList.remove('container--hidden');
        createMessageSelectList(msgList, 4);
    }

    msgGroup = group;
}
/* Allow 'window' context to reference the function */
window.selectMessageGroup = selectMessageGroup;

// Select Message
export function selectMessage(msg) {
    let groupCont = null;
    if (msgGroup == 'cg') {
        groupCont = document.querySelector('.container-smswhapp-group--control');
        groupCont.querySelectorAll('.container-smswhapp-sms').forEach((msgCont) => {
            if (msgCont.getAttribute('data-value-sms') == msg) {
                msgCont.classList.remove('container--hidden');
            } else {
                msgCont.classList.add('container--hidden');
            }
        });
    } else if (msgGroup == 'tg') {
        groupCont = document.querySelector('.container-smswhapp-group--treatment');
        groupCont.querySelectorAll('.container-smswhapp-sms').forEach((msgCont) => {
            if (msgCont.getAttribute('data-value-sms') == msg) {
                msgCont.classList.remove('container--hidden');
            } else {
                msgCont.classList.add('container--hidden');
            }
        });
    } else if (msgGroup == 'sg') {
        groupCont = document.querySelector('.container-smswhapp-group--stakeholder');
        groupCont.querySelectorAll('.container-smswhapp-sms').forEach((msgCont) => {
            if (msgCont.getAttribute('data-value-sms') == msg) {
                msgCont.classList.remove('container--hidden');
            } else {
                msgCont.classList.add('container--hidden');
            }
        });
    } else if (msgGroup == 'dg') {
        groupCont = document.querySelector('.container-smswhapp-group--developer');
        groupCont.querySelectorAll('.container-smswhapp-sms').forEach((msgCont) => {
            if (msgCont.getAttribute('data-value-sms') == msg) {
                msgCont.classList.remove('container--hidden');
            } else {
                msgCont.classList.add('container--hidden');
            }
        });
    }
}
/* Allow 'window' context to reference the function */
window.selectMessage = selectMessage;

// Send Messages
export function sendMessages() {
    console.log('ENVIANDO MENSAJE!');
    let apiUrl = '/sendWASMS/';
    let postData = {
        'date': mdcAssignedVars['selDate'].value.trim() || null,
        'group': mdcAssignedVars['selGroup'].value.trim() || null,
        'msg': mdcAssignedVars['selMessages'].value.trim() || null,
        'msgxm': mdcAssignedVars['selMsgsMins'].value.trim() || null,
        'phone': mdcAssignedVars['selTelNumber'].value.trim() || null
    };

    document.getElementById('submitSaveButton').disabled = true;
    
    postFetch(apiUrl, postData).then((data) => {
        if (data.status == 200) {
            showSBMsg(data.msg, 'success');
            document.getElementById('submitSaveButton').disabled = false;
        } else {
            showSBMsg(data.msg, 'error');
        }
    }).catch((error) => {
        showSBMsg(error, 'error');
    });
}
/* Allow 'window' context to reference the function */
window.sendMessages = sendMessages;

// Show Snackbar Error Message
const appointmentSB = {
    'actionHandler': () => { console.log('Appointment Snackbar Message...'); },
    'actionText': 'OK',
    'message': 'Default message...',
    'showError': false,
    'showSuccess': false,
    'timeout': 7000
};
function showSBMsg(msg, state = null, actionHandler = null, actionHandlerArg = null) {
    // Show Error, Success or No Prefix
    if (state && state == 'error') {
        appointmentSB.showError = true;
        appointmentSB.showSuccess = false;
    } else if (state && state == 'success') {
        appointmentSB.showError = false;
        appointmentSB.showSuccess = true;
    } else {
        appointmentSB.showError = false;
        appointmentSB.showSuccess = false;
    }
    // Assign appropriate Action Handler Type
    if (actionHandler && actionHandler == 'redirect' && actionHandlerArg) {
        // Redirect to URL
        appointmentSB.actionHandler = () => {
            window.location.assign(actionHandlerArg);
        };
    } else if (actionHandler && actionHandler == 'scroll' && actionHandlerArg) {
        // Scroll View to Error Section Element
        appointmentSB.actionHandler = () => {
            actionHandlerArg.scrollIntoView();
        };
    } else {
        appointmentSB.actionHandler = () => {
            console.log('Appointment Snackbar Message...');
        };
    }
    // Message for the Snackbar
    appointmentSB.message = msg;
    initSnackbar(null, appointmentSB);
}

// Snackbar init function
let sbCurrEvent = null;
export function initSnackbar(sb, initObject) {
    if (!sb) sb = snackbar;
    if (sb.isOpen) {
        sb.close('New snackbar initialization...');
    }
    if (sbCurrEvent) {
        sb.unlisten('MDCSnackbar:closed', sbCurrEvent);
    }
    if ('showError' in initObject && initObject.showError) {
        sb.foundation_.adapter_.addClass('mdc-snackbar__label-error-show');
    } else {
        sb.foundation_.adapter_.removeClass('mdc-snackbar__label-error-show');
    }
    if ('showSuccess' in initObject && initObject.showSuccess) {
        sb.foundation_.adapter_.addClass('mdc-snackbar__label-success-show');
    } else {
        sb.foundation_.adapter_.removeClass('mdc-snackbar__label-success-show');
    }

    sb.labelText = initObject.message;
    sb.actionButtonText = initObject.actionText;
    sb.timeoutMs = initObject.timeout;
    sbCurrEvent = ((evt) => {
        if (evt.detail.reason == 'action') {
            initObject.actionHandler();
        }
    });
    sb.listen('MDCSnackbar:closed', sbCurrEvent);
    sb.open();
}
/* Allow 'window' context to reference the function */
window.initSnackbar = initSnackbar;


// Social Media Share Redirect
// Applications URLs
const emailShareUrl = "mailto:?body=";
const facebookShareUrl = "https://www.facebook.com/sharer/sharer.php?u=";
const googlePlusShareURL = "https://plus.google.com/share?url=";
const linkedInShareURL = "https://www.linkedin.com/shareArticle?mini=true&url=";
const twitterShareURL = "https://twitter.com/share?ref_src=twsrc%5Etfw&text=";
const whatsAppShareURL = "https://wa.me/?text=";
export function shareRedirect(e) {
    // Default text of the share message
    var shareText = "¡Mira lo que encontré!";
    shareText = encodeURIComponent(shareText);

    // Share parameters
    var shareMyURL = location.href;
    shareMyURL = encodeURIComponent(shareMyURL);

    var shareTitle = document.title;
    shareTitle = encodeURIComponent(shareTitle);

    // Open a new window to share the content
    var shareAppName = e.detail.item.getElementsByClassName('mdc-list-item__text')[0].textContent;
    shareAppName = shareAppName.toLowerCase().trim();

    switch (shareAppName) {
        case 'email':
            window.open(emailShareUrl + shareTitle + " - " + shareMyURL + "&subject=" + shareText + " - " + shareTitle);
            break;
        case 'facebook':
            window.open(facebookShareUrl + shareMyURL);
            break;
        case 'google+':
            window.open(googlePlusShareURL + shareMyURL);
            break;
        case 'linkedin':
            window.open(linkedInShareURL + shareMyURL + "&title=" + shareTitle);
            break;
        case 'twitter':
            window.open(twitterShareURL + shareText + " - " + shareTitle + ": " + shareMyURL);
            break;
        case 'whatsapp':
            window.open(whatsAppShareURL + shareText + " - " + shareTitle + ": " + shareMyURL);
            break;
        default:
            console.log("No implementation for SHARING to app named: " + shareAppName);
    }
}


/************************** LIBRARIES INIT **************************/

// Initialize AOS
// AOS.init();


/************************** MATERIAL DESIGN COMPONENTS INIT **************************/

// Material Dialog
var assignedDialogEl = document.querySelector('#assigned-dialog');
if (assignedDialogEl) {
    mdcAssignedDialogEl = new MDCDialog(assignedDialogEl);
}

var disconnectedDialogEl = document.querySelector('#disconnected-dialog');
if (disconnectedDialogEl) {
    mdcDisconnectedDialogEl = new MDCDialog(disconnectedDialogEl);
}

var endRTCDialogEl = document.querySelector('#endrtc-dialog');
if (endRTCDialogEl) {
    mdcEndRTCDialogEl = new MDCDialog(endRTCDialogEl);
}

var transferDialogEl = document.querySelector('#transfer-dialog');
if (transferDialogEl) {
    mdcTransferDialogEl = new MDCDialog(transferDialogEl);
}


// Material Drawer & Top App Bar
const drawerEl = document.querySelector('.mdc-drawer');
const topAppBarEl = document.querySelector('.mdc-top-app-bar');
const topAppBarNavEl = document.querySelector('.mdc-top-app-bar__navigation-icon');
if (drawerEl && topAppBarEl) {
    const mainContentEl = document.querySelector('.mdc-drawer-app-content');
    const drawerItemsEl = document.querySelector('.mdc-drawer__content .mdc-list');

    const topAppBar = MDCTopAppBar.attachTo(topAppBarEl);
    topAppBar.setScrollTarget(mainContentEl);

    let isDrawerModal = false;
    let drawerItemHref = null;
    let isHrefNoHistory = false;

    const initModalDrawer = () => {
        isDrawerModal = true;
        drawerEl.classList.add("mdc-drawer--modal");
        topAppBarNavEl.classList.remove("mdc-top-app-bar__navigation-icon--hidden");

        const drawer = MDCDrawer.attachTo(drawerEl);
        drawer.open = false;

        topAppBar.listen('MDCTopAppBar:nav', () => {
            drawer.open = !drawer.open;
        });

        document.body.addEventListener('MDCDrawer:closed', () => {
            drawer.handleScrimClick;
            mainContentEl.querySelector('input, button').focus();
            if (drawerItemHref) {
                if (isHrefNoHistory) {
                    window.location.replace(drawerItemHref);
                } else {
                    window.location.assign(drawerItemHref);
                }
            }
        });

        return drawer;
    }

    const initPermanentDrawer = () => {
        isDrawerModal = false;
        drawerEl.classList.remove("mdc-drawer--modal");
        topAppBarNavEl.classList.add("mdc-top-app-bar__navigation-icon--hidden");

        const permDrawerList = new MDCList(drawerItemsEl);
        permDrawerList.wrapFocus = true;

        return permDrawerList;
    }

    let drawer = window.matchMedia("(max-width: 52.49em)").matches ? initModalDrawer() : initPermanentDrawer();
    
    drawerItemsEl.addEventListener('click', (event) => {
        drawerItemHref = event.target.href;
        isHrefNoHistory = event.target.hasAttribute('data-no-history');
        if (isDrawerModal) {
            drawer.open = false;
            event.preventDefault();
        } else {
            if (isHrefNoHistory) {
                event.preventDefault();
                window.location.replace(drawerItemHref);
            }
        }
    });

    // Toggle between permanent drawer and modal drawer at breakpoint 52.49em
    const resizeHandler = () => {
        if (window.matchMedia("(max-width: 52.49em)").matches && drawer instanceof MDCList) {
            drawer.destroy();
            drawer = initModalDrawer();
        } else if (window.matchMedia("(min-width: 52.5em)").matches && drawer instanceof MDCDrawer) {
            drawer.destroy();
            drawer = initPermanentDrawer();
        }
    }

    window.addEventListener('resize', resizeHandler);

    const myURL = location.pathname;

    Array.from(drawerItemsEl.children).forEach((child, index) => {
        let menuURL = child.getAttribute('href');
        if (menuURL != null && menuURL == myURL) {
            child.classList.add("mdc-list-item--activated");
        }
    });
} else if (topAppBarEl) {
    const topAppBar = MDCTopAppBar.attachTo(topAppBarEl);
    const mainContentEl = document.querySelector('.mdc-drawer-app-content');

    topAppBar.setScrollTarget(mainContentEl);
    topAppBarNavEl.classList.add("mdc-top-app-bar__navigation-icon--hidden");
}


// Material Floating Labels
var mdcFloatingLabels = [].map.call(document.querySelectorAll('.mdc-floating-label'), function (el) {
    return new MDCFloatingLabel(el);
});


// Material Image List Open Image
if (document.querySelector('.mdc-image-list__image')) {
    Array.from(document.getElementsByClassName('mdc-image-list__image')).forEach((elem) => {
        elem.addEventListener('click', () => (window.open(elem.getAttribute('src'))));
    });
}


// Material Line Ripples
var mdcLineRipples = [].map.call(document.querySelectorAll('.mdc-line-ripple'), function (el) {
    return new MDCLineRipple(el);
});


// Material Linear Progress
export const mdcTopBarLoading = new MDCLinearProgress(document.querySelector('.s-topbar-loading'));

var mdcLinearProgress = [].map.call(document.querySelectorAll('.mdc-linear-progress:not(.s-topbar-loading)'), function (el) {
    return new MDCLinearProgress(el);
});


// Material Lists
var mdcLists = [].map.call(document.querySelectorAll('.mdc-list:not(.mdc-menu__items):not(.mdc-select__list)'), function (el) {
    let elList = new MDCList(el);
    let elID = el.getAttribute('id');
    let actionFn = el.getAttribute('data-action-fn');
    if (actionFn) {
        let fn = (typeof actionFn == "string") ? window[actionFn] : actionFn;
        elList.listen('MDCList:action', (evt) => fn(elID, evt.detail.index));
    }
    return elList.listElements.map((listItemEl) => new MDCRipple(listItemEl));
});


// Material Menu
var shareMenu = null;
var shareMenuButton = null;
if (document.querySelector('#shareMenu')) {
    shareMenu = new MDCMenu(document.querySelector('#shareMenu'));
    shareMenuButton = document.querySelector('#shareButton');
}
if (shareMenuButton != null) {
    shareMenuButton.addEventListener('click', () => (shareMenu.open = !shareMenu.open));
    shareMenu.setAnchorCorner(Corner.BOTTOM_START);
    document.querySelector('#shareMenu').addEventListener('MDCMenu:selected', evt => shareRedirect(evt));
}


// Material Notched Outline
var mdcNotchedOutlines = [].map.call(document.querySelectorAll('.mdc-notched-outline'), function (el) {
    return new MDCNotchedOutline(el);
});


// Material Radio Buttons
var mdcRadioButtons = [].map.call(document.querySelectorAll('.mdc-radio'), function (el) {
    return new MDCRadio(el);
});


// Material Ripple
let mdcButtonRipples = [].map.call(document.querySelectorAll('.mdc-icon-button'), function (el) {
    return new MDCRipple(el);
});
mdcButtonRipples.forEach((elem) => {
    elem.unbounded = true;
});
mdcButtonRipples = mdcButtonRipples.concat([].map.call(document.querySelectorAll('.mdc-button, .mdc-fab'), function (el) {
    return new MDCRipple(el);
}));


// Material Snackbar
const snackbar = new MDCSnackbar(document.querySelector('.mdc-snackbar'));


// Material Selects
export var mdcSelects = [].map.call(document.querySelectorAll('.mdc-select'), function (el) {
    let mdcSel = new MDCSelect(el);
    let actionFn = el.getAttribute('data-action-fn');
    if (actionFn) {
        let fn = (typeof actionFn == "string") ? window[actionFn] : actionFn;
        mdcSel.listen('MDCSelect:change', () => fn(mdcSel.value));
    }
    if (el.hasAttribute('data-assigned-var')) {
        MDCSelect.prototype.assignedVar = null;
        mdcSel.assignedVar = el.getAttribute('id');
    }
    return mdcSel;
});


// Material Tab
var mdcTabBars = [].map.call(document.querySelectorAll('.mdc-tab-bar'), function (el) {
    let mdcTab = new MDCTabBar(el);
    let actionFn = el.getAttribute('data-action-fn');
    if (actionFn) {
        let fn = (typeof actionFn == "string") ? window[actionFn] : actionFn;
        mdcTab.listen('MDCTabBar:activated', (evt) => fn(evt.detail.index));
    }
    if (el.hasAttribute('data-assigned-var')) {
        MDCTabBar.prototype.assignedVar = null;
        mdcTab.assignedVar = el.getAttribute('id');
    }
    return mdcTab;
});
// document.querySelector('#mdc-tab-bar__id-noticias').addEventListener('MDCTabBar:activated', evt => showTabContent(evt));


// Material Textfields
export var mdcTextInputs = [].map.call(document.querySelectorAll('.mdc-text-field'), function (el) {
    let mdcTxt = new MDCTextField(el);
    if (el.hasAttribute('data-assigned-var')) {
        MDCTextField.prototype.assignedVar = null;
        mdcTxt.assignedVar = el.getAttribute('id');
    }
    return mdcTxt;
});


// Material Textfields Helper Text
var mdcTFHelperTexts = [].map.call(document.querySelectorAll('.mdc-text-field-helper-text'), function (el) {
    return new MDCTextFieldHelperText(el);
});


// Material Textfields Icons
var mdcTextInputsIcons = [].map.call(document.querySelectorAll('.mdc-text-field-icon'), function (el) {
    return new MDCTextFieldIcon(el);
});


// Material Button Element Actions On Click
document.querySelectorAll('.mdc-button[data-action-type], .mdc-icon-button[data-action-type], .mdc-fab[data-action-type]').forEach(buttonEl => {
    let actionType = buttonEl.getAttribute('data-action-type');
    if (actionType == 'redirect') {
        let actionVal = buttonEl.getAttribute('data-action-val');
        buttonEl.addEventListener('click', () => {
            if (buttonEl.hasAttribute('data-no-history')) {
                window.location.replace(actionVal);
            } else {
                window.location.assign(actionVal);
            }
        });
    } else if (actionType == 'submit') {
        let actionFn = buttonEl.getAttribute('data-action-fn');
        let fn = (typeof actionFn == "string") ? window[actionFn] : actionFn;
        buttonEl.addEventListener('click', fn);
    }
});


// Google Maps component
if (document.querySelector('.s-googlemaps')) {
    var gmComp = document.querySelector('.s-googlemaps');
    var gmURLL = 'https://www.google.com/maps?output=embed&daddr=ciudad+mujer&saddr=';
    var gmIfrS = "<iframe src='";
    var gmIfrE = "' class='s-googlemaps__iframe' frameborder='0' style='border:0;' allowfullscreen></iframe>";
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            gmComp.innerHTML = "";
            gmComp.innerHTML = gmIfrS + gmURLL + pos.lat + ',' + pos.lng + gmIfrE;
        }, () => {
            console.log('User denied access to location');
        });
    } else {
        // Browser doesn't support Geolocation
        console.log('Your browser does not support Geolocation');
    }
}


/************************** PWA SERVICE WORKER INIT **************************/

// Registering the service worker for the pwa
// NOTE
// Even though this service worker is not on the root of this web application
// It has been configured, through swing_main.py to make it look like it is.


// Instance of Local Storage to retrieve SW Version
const swStore = localforage.createInstance({
    name: 'swingcms-sw'
});


// Evaluate if Browser accepts Service Workers
if ('serviceWorker' in navigator) {
    const wb = new Workbox('/sw.js', { scope: '/' });
    // Detects an update for the app's content and prompts user to refresh
    wb.addEventListener('installed', event => {
        // Retrieve SW version
        let swVerEl = document.querySelector('#s-version');
        if (swVerEl) {
            swStore.getItem('swVersion').then( (val) => {
                swVerEl.textContent = val;
            });
        }
        
        if (event.isUpdate) {
            console.log('App update found...');
            initSnackbar(snackbar, updateSBDataObj);
        }
    });
    // Registers the Workbox Service Worker
    wb.register();
}


// Add to Homescreen (A2H) Event
let deferredPrompt;
var appIsInstalled = false;

// Snackbar A2H Data for Install Event
const installSBDataObj = {
    message: '¿Deseas Instalar nuestra App? (¡Gratis!)',
    actionText: 'Si',
    timeout: 10000,
    actionHandler: () => {
        console.log('Installing app (A2H)...');
        // Show the prompt
        deferredPrompt.prompt();
        // Wait for the user action
        deferredPrompt.userChoice
            .then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('User accepted the A2H prompt');
                    appIsInstalled = true;
                } else {
                    console.log('User dismissed the A2H prompt');
                }
                deferredPrompt = null;
            });
    }
};


// Snackbar Data for Update Website Event
const updateSBDataObj = {
    message: '¡Nuevo contenido disponible!. Click OK para actualizar.',
    actionText: 'OK',
    timeout: 10000,
    actionHandler: () => {
        console.log('Updating app...');
        // Refresh the app
        window.location.reload();
    }
};


window.addEventListener('appinstalled', (evt) => {
    console.log('App is installed...');
    appIsInstalled = true;
});


window.addEventListener('beforeinstallprompt', (e) => {
    console.log('Prompting to install app...');
    // Prevent Chrome 67 and earlier from automatically showing the prompt
    e.preventDefault();
    // Stash the event so it can be triggered later.
    deferredPrompt = e;
    // Show the Snackbar popup to Install
    if (!appIsInstalled) {
        initSnackbar(snackbar, installSBDataObj);
    }
});


// Show SW Version
let swVerEl = document.querySelector('#s-version');
if (swVerEl) {
    // Retrieve SW version
    swStore.getItem('swVersion').then( (val) => {
        if (val) {
            swVerEl.textContent = val;
        }
    });
}


// MDC Assigned Components to Variables
// This is done to reference specific MDC instantiated elements, their properties and functions
export const mdcAssignedVars = {};

window.addEventListener('load', () => {
    // Store MDC Elements to Assigned Variables Object
    mdcSelects.forEach((sel) => {
        if (sel.assignedVar)
            mdcAssignedVars[sel.assignedVar] = sel;
    });

    mdcTextInputs.forEach((txt) => {
        if (txt.assignedVar)
            mdcAssignedVars[txt.assignedVar] = txt;
    });
});
