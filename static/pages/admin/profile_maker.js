const vue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        // BASE_URL: 'http://localhost:8000/',
        form: {
            company_name: '',
            email: '',
            phone: '',
            password: '',
            city: '',
            state: '',
            address: '',
            username_type: ['email'],
            available_series: [],
        },
        options: [
            {text: 'ایمیل', value: 'email'},
            {text: 'شماره تماس', value: 'phone'}
        ],
        series_options: [],
        req_msg: 'اطلاعات وارد شده غلط می‌باشد. دوباره تلاش کنید',
        alert_header: ' ورود ناموفقیت آمیز',
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

        returnToPanel: function(){
            window.location.href = this.BASE_URL + 'admin/dashboard'
        },

        show_alert(msg){
            this.req_msg = msg;
            this.$bvToast.show('req');
        },

        check_form_validation() {
            if (this.form.company_name !== '' && this.form.password.length >= 8
                && this.form.address !== '' && (this.form.phone !== '' || this.form.email !== '')){
                return true
            }
            return false
        },

        submit_data() {
            if (!this.check_form_validation()) {
                return
            }
            axios({
                method: 'post',
                url: this.BASE_URL + 'admin/submit_customer/',
                headers: {
                    "X-CSRFToken": this.getCookie('csrftoken'),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                data: {
                    'form': this.form
                }
            }).then(response => {
                if (response.status === 200) this.show_alert('ثبت نام با موفقیت انجام شد');
                else this.show_alert('ثبت نام به مشکل بر خورد')
            }).catch(response => this.show_alert('مشکلی در سرور بوجود آمد'))
        }
    },
    computed: {
      state() {
        return this.form.username_type.length > 0
      }
    },
    created(){
        axios({
            method: 'get',
            url: this.BASE_URL + 'admin/product_series/'
        }).then(response => {
            if (response.status === 200){
                this.series_options = response.data.products;
                this.form.available_series = response.data.products;
            } else{
                this.show_alert('صفحه به درستی بارگزاری نشد')
            }
        }).catch(response => this.show_alert('صفحه به درستی بارگزاری نشد'))
    }
});