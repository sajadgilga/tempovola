const vue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        // BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        BASE_URL: 'http://localhost:8000/',
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
            melodies: {}
        },
        options: [
            {text: 'ایمیل', value: 'email'},
            {text: 'شماره تماس', value: 'phone'}
        ],
        series_options: [],
        melody_options: {},
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
                this.show_alert("فیلد های لازم را پر کنید");
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
                else this.show_alert(response.data.msg)
            }).catch(response => this.show_alert("ایمیل یا شماره تلفن تکراری است"))
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
                response.data.products.forEach(item => {
                    if(Object.keys(this.melody_options).includes(item[0])){
                        this.melody_options[item[0]].push(item[1]);
                    }else {
                        this.melody_options[item[0]] = [item[1]];
                    }
                });
                this.series_options = Object.keys(this.melody_options);
                this.form.available_series = this.series_options;
                this.form.melodies = Object.assign({}, this.melody_options);
            } else{
                this.show_alert('صفحه به درستی بارگزاری نشد')
            }

            document.querySelector('div').classList.remove('hid');
        }).catch(response => this.show_alert('صفحه به درستی بارگزاری نشد'))
    }
});