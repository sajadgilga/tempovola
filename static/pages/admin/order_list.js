const vue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        // BASE_URL: 'http://localhost:8000/',
        req_msg: '',
        alert_header: ' ورود ناموفقیت آمیز',
        data: {},
        fields: [
            'وضعیت',
            'تاریخ ارسال',
            'تاریخ تایید',
            'تاریخ تغییر',
            'تاریخ سفارش',
            'آدرس ارسال',
            'نام خریدار',
            'هزینه سفارش',
            'کد سفارش',
            'ردیف',
        ],
        orders: [],
    },
    methods: {
        addData(data){
            this.data = data;
            this.orders = this.data.orders.reverse()
        },

        returnToPanel: function(){
            window.location.href = this.BASE_URL + 'admin/dashboard'
        },

        show_alert(msg){
            this.req_msg = msg;
            this.$bvToast.show('req');
        },

        boolean_converter(value){
            if (value === true)
                return 'تایید شده'
            else
                return 'تایید نشده'
        }
    },
    created(){
        axios({
            method: 'get',
            url: this.BASE_URL + 'admin/fetch_orders',
            headers: {
                'Accept': 'Application/json',
                'Content_Type': 'Application/json'
            }
        }).then(respond => {
            if (respond.status === 200)
                this.addData(respond.data);
            else
                this.show_alert('عدم دریافت اطلاعات از سرور');

            document.querySelector('div').classList.remove('hid');
        }).catch(respond => {
            this.show_alert("اطلاعات از سرور دریافت نشد")
        })
    }
});
