var vue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        // BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        // BASE_URL: 'http://localhost:8000/',
                BASE_URL: 'http://86.104.32.238:8000/',

        show: false,
        is_username_valid: null,
        is_pass_valid: null,
        username: '',
        password: '',
        user_msg: 'ایمیل یا شماره موبایل اشتباه وارد شده',
        pass_msg: 'رمز عبور را وارد کنید',
        login_failed: true,
        username_type: 'email',
        isValid: 'outline-dark',
        btn_valid_state: 'success',
        btn_invalid_state: 'outline-dark',
        countDown: 0,
        dismissSec: 3,
        alert_msg: '',
        login_result: 'danger',
        alert_header: ' ورود ناموفقیت آمیز',
    },
    methods: {
        show_alert: function () {
             this.$bvToast.show('req');
        },

        getCookie: function (name) {
            if (!document.cookie) {
                return null;
            }

            const xsrfCookies = document.cookie.split(';')
                .map(c => c.trim())
                .filter(c => c.startsWith(name + '='));

            if (xsrfCookies.length === 0) {
                return null;
            }

            return decodeURIComponent(xsrfCookies[0].split('=')[1]);
        },

        check_form_validation: function () {
            if (this.is_pass_valid && this.is_username_valid) {
                this.isValid = this.btn_valid_state;
                return true;
            }
            if (!this.is_pass_valid)
                this.is_pass_valid = false;
            if (!this.is_username_valid)
                this.is_username_valid = false;
            this.isValid = this.btn_invalid_state;
            return false;
        },


        login: function () {
            if (!this.check_form_validation())
                return;
            axios({
                method: 'post',
                url: this.BASE_URL + 'customer/login/',
                headers: {
                    "X-CSRFToken": this.getCookie('CSRF-TOKEN'),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                data: {
                    'username': this.username,
                    'password': this.password
                }
            }).then(response => this.verify_login(response))
                .catch(response => this.verify_login(response))
        },

        verify_login: function (response) {
            if (response.status === 200) {
                this.alert_msg = 'با موفقیت وارد شدید';
                this.login_result = 'success';
                this.alert_header = 'ورود موفقیت آمیز';
                this.show_alert();
                setInterval(() => window.location.assign(this.BASE_URL + 'customer/shop/'), 1000)
            }
             else {
                 if (response.data != null) {
                     this.alert_msg = response.data.msg;
                 } else if (response.response.status === 403){
                     axios({
                         method: 'get',
                         url: this.BASE_URL + 'customer/logout/'
                     }).then(response => this.login()).catch(response => (console.log('problem in logging out of last session')))
                 } else if (response.response.status === 401){
                     this.alert_msg = response.response.data.msg;
                 } else {
                     this.alert_msg = 'مشکلی در سرور به وجود آمده'
                 }
                this.login_result = 'danger';
                this.alert_header = ' ورود ناموفقیت آمیز';
                this.show_alert()
            }
        },
    },
    computed: {
        pass_state: function () {
            if (this.is_pass_valid === null && this.password.length === 0)
                return null;
            this.is_pass_valid = this.password.length > 0;
            return this.is_pass_valid;
        },

        login_state: function () {
            if (this.is_username_valid === null && this.username.length === 0)
                return null;
            var email_pattern = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            var mobile_patterns = [/^\(?([0-9]{4})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/, /^\+?([0-9]{2})\)?[-. ]?([0-9]{5})[-. ]?([0-9]{5})$/];
            if (email_pattern.test(this.username.toLocaleLowerCase())) {
                this.username_type = 'email';
                this.is_username_valid = true;
            } else if (mobile_patterns[0].test(this.username) || mobile_patterns[1].test(this.username)) {
                this.username_type = 'text';
                this.is_username_valid = true;
            } else
                this.is_username_valid = false;
            return this.is_username_valid;
        },

    },
    watch: {
        is_username_valid: function () {
            this.check_form_validation()
        },

        is_pass_valid: function () {
            this.check_form_validation()
        }
    }
});