import Link from 'next/link';

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <div className="flex space-x-4">
          <Link
            href="/invoices/new"
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
          >
            Create Invoice
          </Link>
          <Link
            href="/clients/new"
            className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors"
          >
            Add Client
          </Link>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <span className="text-2xl">📄</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Invoices</p>
              <p className="text-2xl font-bold text-gray-900">--</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <span className="text-2xl">💰</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Revenue</p>
              <p className="text-2xl font-bold text-gray-900">$--</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <span className="text-2xl">⏳</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Pending Amount</p>
              <p className="text-2xl font-bold text-gray-900">$--</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <span className="text-2xl">👥</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Clients</p>
              <p className="text-2xl font-bold text-gray-900">--</p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Invoices */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Recent Invoices</h2>
            <Link href="/invoices" className="text-blue-600 hover:text-blue-800 text-sm">
              View all
            </Link>
          </div>
          <div className="space-y-3">
            <div className="text-center py-8 text-gray-500">
              <span className="text-4xl mb-2 block">📄</span>
              <p>No invoices yet</p>
              <Link href="/invoices/new" className="text-blue-600 hover:text-blue-800 text-sm">
                Create your first invoice
              </Link>
            </div>
          </div>
        </div>

        {/* Recent Payments */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Recent Payments</h2>
            <Link href="/payments" className="text-blue-600 hover:text-blue-800 text-sm">
              View all
            </Link>
          </div>
          <div className="space-y-3">
            <div className="text-center py-8 text-gray-500">
              <span className="text-4xl mb-2 block">💳</span>
              <p>No payments yet</p>
              <Link href="/payments/new" className="text-blue-600 hover:text-blue-800 text-sm">
                Record a payment
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Link
            href="/invoices/new"
            className="flex flex-col items-center p-4 border rounded-lg hover:bg-gray-50 transition-colors"
          >
            <span className="text-2xl mb-2">📄</span>
            <span className="text-sm font-medium">New Invoice</span>
          </Link>
          <Link
            href="/clients/new"
            className="flex flex-col items-center p-4 border rounded-lg hover:bg-gray-50 transition-colors"
          >
            <span className="text-2xl mb-2">👤</span>
            <span className="text-sm font-medium">Add Client</span>
          </Link>
          <Link
            href="/payments/new"
            className="flex flex-col items-center p-4 border rounded-lg hover:bg-gray-50 transition-colors"
          >
            <span className="text-2xl mb-2">💳</span>
            <span className="text-sm font-medium">Record Payment</span>
          </Link>
          <Link
            href="/invoices"
            className="flex flex-col items-center p-4 border rounded-lg hover:bg-gray-50 transition-colors"
          >
            <span className="text-2xl mb-2">📊</span>
            <span className="text-sm font-medium">View Reports</span>
          </Link>
        </div>
      </div>
    </div>
  );
} 