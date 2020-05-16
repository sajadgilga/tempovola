const vue = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        // BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        BASE_URL: 'http://130.185.74.195/',
        // BASE_URL: 'http://localhost:8000/',
        req_msg: '',
    },
    methods: {
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

        logout: function () {
            axios({
                method: 'get',
                url: this.BASE_URL + 'admin/logout/'
            }).then(response => {
                this.show_alert('با موفقیت خارج شدید');
                window.location.replace(this.BASE_URL + 'admin/')
            })
                .catch(response => this.show_alert('مشکل در خروج بوجود آمده. لطفا دوباره تلاش کنید'))
        },

        returnToPanel: function () {
            window.location.href = this.BASE_URL + 'admin/dashboard'
        },

        show_alert(msg) {
            this.req_msg = msg;
            this.$bvToast.show('req');
        },

        showLogs(user) {
            axios({
                method: 'post',
                url: this.BASE_URL + '/admin/get_admin_logs/',
                headers: {
                    'Content_Type': 'Application/json',
                    "X-CSRFToken": this.getCookie('csrftoken')
                },
                data: {
                    username: user
                }
            }).then(response => {
                if (response.status === 200) {

                } else this.show_alert('درخواست شما به مشکل برخورد')
            }).catch(reason => {
                this.show_alert('درخواست شما به مشکل برخورد')
            })
        }

    }
});
