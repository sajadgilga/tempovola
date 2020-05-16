const vue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        // BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        BASE_URL: 'http://130.185.74.195/',
        // BASE_URL: 'http://localhost:8000/',
        req_msg: '',
        data: [],
        fields: [
            {key: 'send', label: 'ارسال پاسخ'},
            {key: 'reply', label: 'پاسخ'},
            {key: 'request', label: 'درخواست'},
            {key: 'email', label: 'ایمیل مشتری'},
            {key: 'name', label: 'نام مشتری'},
            {key: 'date', label: 'تاریخ ارسال'},
            {key: 'index', label: 'ردیف'},
        ],
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

        addReports(data) {
            this.data = data.reports
            console.log('d')
        },

        sendAnswer(idx) {
            axios({
                method: 'post',
                url: this.BASE_URL + 'admin/send_customer_report_answer/',
                headers: {
                    'Content_Type': 'Application/json',
                    "X-CSRFToken": this.getCookie('csrftoken')
                },
                data: {
                    report: this.data[idx]
                }
            }).then(response => {
                if (response.status === 200) {
                    this.data[idx].is_active = false
                } else
                    this.show_alert('پاسخ ارسال نشد')
            }).catch(reason => this.show_alert('پاسخ ارسال نشد'))
        }

    },
    created() {
        axios({
            method: 'get',
            url: this.BASE_URL + 'admin/get_customer_reports/'
        }).then((response) => this.addReports(response.data))
    }
});