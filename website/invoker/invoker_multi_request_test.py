from django.test import TestCase
from unittest.mock import patch, Mock

from invoker.invoker_multi_request import InvokerMultiRequest, Priority
from invoker.invoker_request import InvokerRequest
from invoker.models import InvokerReport
from invoker.invoker import Invoker, InvokerProcess


class TestInvokerMultiRequest(TestCase):
    @patch("invoker.invoker_multi_request.InvokerRequest")
    @patch("invoker.invoker_multi_request.InvokerMultiRequestPriorityQueue")
    def test_start(self, mock_queue: Mock, mock_request: Mock):
        invoker_multi_request = InvokerMultiRequest([mock_request])
        invoker_multi_request.start()
        mock_queue = mock_queue()
        mock_add = mock_queue.add
        mock_add.assert_called_with(invoker_multi_request)

    @patch("invoker.invoker.Invoker")
    @patch("invoker.invoker_multi_request.InvokerRequest")
    def test_run(self, mock_request: Mock, mock_invoker: Mock):
        invoker_requests = [mock_request() for _ in range(3)]
        invokers = [mock_invoker() for _ in range(3)]

        invoker_multi_request = InvokerMultiRequest(invoker_requests)
        invoker_multi_request.run(invokers)

        for (invoker, request) in zip(invokers, invoker_requests):
            request.run.assert_called_with(invoker)

    @patch("invoker.invoker_multi_request.InvokerRequest")
    def test_notify(self, mock_request: Mock):
        mock_notify = Mock()

        invoker_report = InvokerReport()

        invoker_multi_request = InvokerMultiRequest([mock_request])
        invoker_multi_request.subscribe_to_reports(mock_notify)

        invoker_multi_request.notify(invoker_report)
        mock_notify.assert_called()

    @patch("invoker.invoker_multi_request.InvokerRequest")
    def test_not_all_notify(self, mock_request: Mock):
        mock_notify = Mock()

        invoker_requests = [mock_request for _ in range(2)]
        invoker_report = InvokerReport()

        invoker_multi_request = InvokerMultiRequest(invoker_requests)
        invoker_multi_request.subscribe_to_reports(mock_notify)

        invoker_multi_request.notify(invoker_report)
        mock_notify.assert_not_called()

    @patch("invoker.invoker_multi_request.InvokerRequest")
    def test_all_notify(self, mock_request: Mock):
        mock_notify = Mock()

        invoker_requests = [mock_request for _ in range(3)]
        invoker_reports = [InvokerReport() for _ in range(3)]

        invoker_multi_request = InvokerMultiRequest(invoker_requests)
        invoker_multi_request.subscribe_to_reports(mock_notify)

        for invoker_report in invoker_reports:
            invoker_multi_request.notify(invoker_report)

        mock_notify.assert_called_with(invoker_reports)

    def test_send_processes(self):
        mock = Mock()

        invoker_requests = []
        for index in range(3):
            invoker_requests.append(Mock())
        invoker_process = [Mock() for _ in range(3)]

        for index in range(3):
            invoker_requests[index].process = invoker_process[index]

        invoker_multi_request = InvokerMultiRequest(invoker_requests)
        invoker_multi_request.subscribe_to_processes(mock.notify_processes)

        invoker_multi_request.send_process()

        mock.notify_processes.assert_called_with(invoker_process)

    def test_subscribe(self):
        rep_mock = Mock()
        pro_mock = Mock()
        invoker_multi_request = InvokerMultiRequest([])
        invoker_multi_request.subscribe_to_reports(rep_mock)
        invoker_multi_request.subscribe_to_processes(pro_mock)
        self.assertEqual(invoker_multi_request.report_subscribers[0], rep_mock)
        self.assertEqual(invoker_multi_request.process_subscribers[0], pro_mock)
