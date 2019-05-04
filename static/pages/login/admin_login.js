var vue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        BASE_URL: 'http://localhost:8000/',
        username: '',
        password: '',
        user_msg: 'نام کاربری اشتباه وارد شده',
        pass_msg: 'رمز عبور را وارد کنید',
        login_failed: true,
        alert_msg: 'اطلاعات وارد شده غلط می‌باشد. دوباره تلاش کنید',
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

        login: function () {
            axios({
                method: 'post',
                url: this.BASE_URL + 'admin/login/',
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
                window.location.replace(this.BASE_URL + "admin/dashboard")
            }
             else {
                 if (response.data != null) {
                     this.alert_msg = response.data.msg;
                 } else if (response.response.status === 403){
                     axios({
                         method: 'get',
                         url: this.BASE_URL + 'admin/logout/'
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
});