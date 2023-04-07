import Swal from 'sweetalert2';

class MainHelper {
	loadingAlert() {
		Swal.fire({
			title: 'กรุณารอสักครู่',
			allowOutsideClick: false
		});
		Swal.showLoading();
	}
}

export default new MainHelper()