<template>
	<div class="wrapper">
		<div class="container">
			<div class="row">
				<div class="col-lg-10 col-md-10 col-sm-12 mx-auto">
					<div class="card">
						<strong>แนวนโยบายและแนวปฏิบัติการให้บริการใบรับรองอิเล็กทรอนิกส์</strong>
						<iframe width="100%" height="650px"
						:src="pdfFile+'#page=1&zoom=100&toolbar=0&navpanes=0&scrollbar=0'">
						</iframe>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import pdfFile from '@/assets/pdf/แนวนโยบายและแนวปฏิบัติการให้บริการใบรับรองอิเล็กทรอนิกส์.pdf';

export default {
	name: 'TermAndCondition',
	data() {
		return {
			pdfFile
		}
	}
}
</script>

<style scoped>
.wrapper {
	min-height: 100%;
}
</style>