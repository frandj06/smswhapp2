import { postFetch } from './swing_app';

// FirebaseUI config.
var firebaseUIConfig = {
    callbacks: {
        signInSuccessWithAuthResult: function(authResult, redirectUrl) {
            const user = authResult.user;
            user.getIdToken().then(idToken => {
                var postData = {
                    "idToken": idToken,
                    "csrfToken": "ADMIN123654"
                };
                postFetch('/loginuser/', postData);
            });
        },
        signInFailure: function(error) {
            // Some unrecoverable error occurred during sign-in.
            // Return a promise when error handling is completed and FirebaseUI
            // will reset, clearing any UI. This commonly occurs for error code
            // 'firebaseui/anonymous-upgrade-merge-conflict' when merge conflict
            // occurs. Check below for more details on this.
            return handleUIError(error);
        },
        uiShown: function() {
            // The widget is rendered.
            // Hide the loader.
            document.getElementById('s-loader').style.display = 'none';
        }
    },
    signInSuccessUrl: '/login/',
    signInOptions: [
        // Leave the lines as is for the providers you want to offer your users.
        firebase.auth.GoogleAuthProvider.PROVIDER_ID,
        firebase.auth.FacebookAuthProvider.PROVIDER_ID,
        firebase.auth.EmailAuthProvider.PROVIDER_ID
    ],
    // Terms of service url/callback.
    tosUrl: '/terminosdelservicio/',
    // Privacy policy url/callback.
    privacyPolicyUrl: '/politicaprivacidad/'
}

// Initialize the FirebaseUI Widget using Firebase.
var firebaseUI = new firebaseui.auth.AuthUI(firebase.auth());

// The start method will wait until the DOM is loaded.
if (document.querySelector('#firebaseui-auth-container')) {
    firebaseUI.start('#firebaseui-auth-container', firebaseUIConfig);
}
