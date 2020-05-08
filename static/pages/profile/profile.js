const vue = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        // BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        BASE_URL: 'http://localhost:8000/',
        name: null,
        req_msg: '',
        email: 'tempovola@gmail.com',
        phone: '76983',
        report: '',
        order_fields: [
              { key: 'status', label: 'وضعیت' },
              { key: 'date', label: 'تاریخ سفارش' },
              { key: 'address', label: 'آدرس ارسال' },
              { key: 'cost', label: 'هزینه سفارش' },
              { key: 'code', label: 'کد سفارش' },
              { key: 'index', label: 'ردیف' },
        ],
        report_fields: [
              { key: 'reply', label: 'جواب' },
              { key: 'request', label: 'درخواست' },
              { key: 'date', label:  'تاریخ ارسال' },
        ],
        orders: [],
        reports: []
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

        redirect_to_shop: function () {
            window.location.assign(this.BASE_URL + 'customer/shop');
        },

        send_report: function () {
            if (this.report.length === 0) {
                this.req_msg = 'متن گزارش خالی است';
                this.$bvToast.show('req');
                return
            }
            axios({
                method: 'post',
                url: this.BASE_URL + 'customer/send_report/',
                headers: {
                    "X-CSRFToken": this.getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                data: {
                    'report': this.report,
                }
            }).then(response => {
                this.$bvToast.show('req');
                this.req_msg = 'با موفقیت ارسال شد';
            })
                .catch(reason => {
                    this.req_msg = 'درخواست شما به مشکل برخورد';
                    this.$bvToast.show('req');
                })

        },

        show_reports: function () {
            axios({
                method: 'get',
                url: this.BASE_URL + 'customer/get_orders_report/',
            }).then(response => {
                this.orders = response.data.orders;
                this.reports = response.data.reports;
                this.$bvModal.show('reports');
            }).catch(reason => {
                this.req_msg = 'درخواست شما به مشکل برخورده';
                this.$bvToast.show('req');
            });
        },

        show_orders: function () {
            axios({
                method: 'get',
                url: this.BASE_URL + 'customer/get_orders_report/',
            }).then(response => {
                this.orders = response.data.orders;
                this.reports = response.data.reports;
                this.$bvModal.show('orders');
            }).catch(reason => {
                this.req_msg = 'درخواست شما به مشکل برخورده';
                this.$bvToast.show('req');
            });
        },

        order_status_text: function(status) {
            switch (status) {
                case 0:
                    return 'بررسی سفارش';
                case 1:
                    return 'بررسی سفارش';
                case 2:
                    return 'بررسی مالی';
                case 3:
                    return 'نیاز به پرداخت';
                case 4:
                    return 'آماده ارسال';
                case 5:
                    return 'در دست مدیریت';
                case 7:
                    return 'تحویل شده';
            }
        },

        boolean_converter(value) {
            if (value === true)
                return 'تایید شده'
            else
                return 'تایید نشده'
        },


        logout: function () {
            axios({
                method: 'get',
                url: this.BASE_URL + 'customer/logout/',
            }).then(response => {
                if (response.status === 200) {
                    window.location.replace(this.BASE_URL)
                } else {
                    this.$bvToast.show('req');
                    this.req_msg = 'خروج در حال حاضر ممکن نیست.'
                }
            })
                .catch(response => {
                    this.$bvToast.show('req');
                    this.req_msg = 'خروج در حال حاضر ممکن نیست.'
                })
        }
    },
    created() {
        document.querySelector('div').classList.remove('hid');
    }
});
