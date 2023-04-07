import Swal from 'sweetalert2';

class MainHelper {
	loadingAlert() {
		Swal.fire({
			title: 'กรุณารอสักครู่',
			allowOutsideClick: false
		});
		Swal.showLoading();
	}

	successAlert(message, callback) {
		Swal.fire({
			title: 'สำเร็จ!',
			html: message,
			icon: 'success',
			confirmButtonText: 'ตกลง'
		}).then(() => {
			callback();
		})
	}

	failAlert(message) {
		Swal.fire({
			title: 'ผิดพลาด',
			html: message,
			icon: 'error',
			confirmButtonText: 'ตกลง'
		})
	}
}

export default new MainHelper()