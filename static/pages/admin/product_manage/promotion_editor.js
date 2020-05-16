const vue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        // BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        BASE_URL: 'http://130.185.74.195/',
        // BASE_URL: 'http://localhost:8000/',
        req_msg: '',
        alert_header: ' ورود ناموفقیت آمیز',
        data: {},
        promotion: {
            description: '',
            discount_percent: 0,
            image: null,
            scenarios: []
        },
        scenario_model: {
            type: 'total_count',
            items: null
        },
        fields: [
            'مشاهده',
            'وضعیت',
            'تاریخ سفارش',
            'آدرس ارسال',
            'نام خریدار',
            'هزینه سفارش',
            'کد سفارش',
            'ردیف',
        ],
        promotions: [],

        order_fields: [
            'تعداد مورد تایید',
            'تعداد سفارش شده',
            'هزینه',
            'کد ملودی',
            'ملودی',
            'ردیف',
        ],
        current_processed_order: null,
        currentPage: 1,
        mainTablePerPage: 10
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

        addData(data) {
            this.data = data;
            this.promotions = this.data.promotions
        },

        returnToPanel: function () {
            window.location.href = this.BASE_URL + 'admin/dashboard'
        },

        show_alert(msg) {
            this.req_msg = msg;
            this.$bvToast.show('req');
        },

        see_order(idx) {
            // this.order_items = null;
            // this.order_items = [...this.orders[idx].items];
            // this.order_items = JSON.parse(JSON.stringify(this.orders[idx].items));
            // this.current_processed_order = idx;
            // this.$bvModal.show('order_manager');
        },

        boolean_converter(value) {
            if (value === true)
                return 'تایید شده';
            else
                return 'تایید نشده';
        }
    },
    computed: {
        table_rows() {
            return this.orders.length
        }
    }
});
