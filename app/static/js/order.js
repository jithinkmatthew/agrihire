function daysBetween(startDate, endDate) {
  const date1 = new Date(startDate);
  const date2 = new Date(endDate);

  date1.setHours(0, 0, 0, 0);
  date2.setHours(0, 0, 0, 0);

  const diffMilliseconds = date2 - date1;
  // Calculate days difference and add 1 for inclusive count
  return Math.abs(Math.round(diffMilliseconds / (1000 * 60 * 60 * 24))) + 1;
}

function hoursBetween(startDate, endDate) {
  const date1 = new Date(startDate);
  const date2 = new Date(endDate);

  // Calculate difference in milliseconds
  const diffMilliseconds = date2 - date1;

  // Convert milliseconds to hours
  const diffHours = diffMilliseconds / (1000 * 60 * 60);

  return Math.abs(diffHours);
}

function calculateOrderSummary() {

  // Date Elements
  const startDate = document.getElementById('equipment_rental_start_date').value;
  const endDateElement = document.getElementById('equipment_rental_end_date');
  const endDate = endDateElement ? endDateElement.value : null;

  const startTimeEle = document.getElementById('equipment_rental_start_time');
  const startTime = startTimeEle ? startTimeEle.value : null;
  const endTimeEle = document.getElementById('equipment_rental_end_time');
  const endTime = endTimeEle ? endTimeEle.value : null;

  const checkedRadio = document.querySelector("input[name='equipment_delivery_option']:checked");
  const isDelivery = checkedRadio && checkedRadio.value === 'address';

  const orderSummaryContainer = document.getElementById('order-summary');
  const orderSummaryDateSelectMsg = document.getElementById('order-summary-message');
  const rentalDuration = document.getElementById('rental-duration');
  const rate = document.getElementById('equipment-rate');
  const equipmentTotalElement = document.getElementById('equipment-total');
  const deliveryAmountContainer = document.getElementById('equipment-delivery-amount-container');
  const deliveryAmountInput = document.getElementById('equipment-delivery-amount');
  const equipmentGrantTotal = document.getElementById('grand-total-display');

  orderSummaryContainer.style.display = 'none';
  orderSummaryDateSelectMsg.style.display = '';

  // Hourly Mode Equipment caluculation
  if (startTime && endTime) {

    const start = new Date(`${startDate}T${startTime}:00`);
    const end = new Date(`${startDate}T${endTime}:00`);

    if (start > end) {
      alert("Start time must be earlier than end time.");
      return;
    }

    orderSummaryContainer.style.display = '';
    deliveryAmountContainer.style.display = 'none';
    orderSummaryDateSelectMsg.style.display = 'none';

    const duration = hoursBetween(start, end);
    rentalDuration.value = duration;

    const price = parseFloat(rate.value);
    const rentalTotal = duration * price;

    let finalAmount = rentalTotal;

    // Add delivery cost only if delivery option is selected
    if (isDelivery && deliveryAmountInput) {
      deliveryAmountContainer.style.display = '';
      const deliveryCost = parseFloat(deliveryAmountInput.value) || 0;
      finalAmount += deliveryCost;
    }

    // Update summary fields
    equipmentTotalElement.textContent = rentalTotal.toFixed(2);
    equipmentGrantTotal.value = finalAmount.toFixed(2);

    if (equipmentGrantTotal) {
      equipmentGrantTotal.textContent = finalAmount.toFixed(2);
    }
    else {
      orderSummaryContainer.style.display = 'none';
      orderSummaryDateSelectMsg.style.display = '';
    }
  }

  // Daily Mode Equipment caluculation
  if (startDate && endDate) {

    const start = new Date(startDate);
    const end = new Date(endDate);

    if (start > end) {
      alert("Start date must be earlier than end date.");
      return; // Stop calculation
    }

    orderSummaryContainer.style.display = '';
    deliveryAmountContainer.style.display = 'none';
    orderSummaryDateSelectMsg.style.display = 'none';

    const duration = daysBetween(startDate, endDate);
    rentalDuration.value = duration;

    const price = parseFloat(rate.value);
    const rentalTotal = duration * price;

    let finalAmount = rentalTotal;

    // Add delivery cost only if delivery option is selected
    if (isDelivery && deliveryAmountInput) {
      deliveryAmountContainer.style.display = '';
      const deliveryCost = parseFloat(deliveryAmountInput.value) || 0;
      finalAmount += deliveryCost;
    }

    // Update summary fields
    equipmentTotalElement.textContent = rentalTotal.toFixed(2);
    equipmentGrantTotal.value = finalAmount.toFixed(2);

    if (equipmentGrantTotal) {
      equipmentGrantTotal.textContent = finalAmount.toFixed(2);
    }
    else {
      orderSummaryContainer.style.display = 'none';
      orderSummaryDateSelectMsg.style.display = '';
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // Add listeners for delivery method changes
  var radios = document.querySelectorAll("input[name='equipment_delivery_option']");
  radios.forEach(function (radio) {
    radio.addEventListener('change', calculateOrderSummary);
  });

  // Add listeners for date changes
  document.getElementById('equipment_rental_start_date').addEventListener('change', calculateOrderSummary);
  const endDateElement = document.getElementById('equipment_rental_end_date');
  if (endDateElement) {
    endDateElement.addEventListener('change', calculateOrderSummary);
  }

  // Add listeners for time changes
  summaryStartTimeElement = document.getElementById('equipment_rental_start_time');
  if (summaryStartTimeElement) {
    summaryStartTimeElement.addEventListener('change', calculateOrderSummary);
  }

  summaryEndTimeElement = document.getElementById('equipment_rental_end_time');
  if (summaryEndTimeElement) {
    summaryEndTimeElement.addEventListener('change', calculateOrderSummary);
  }

  calculateOrderSummary()
});
