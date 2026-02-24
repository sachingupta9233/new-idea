import React, { useState } from 'react';
import axios from 'axios';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const API_BASE_URL = 'https://new-idea-3.onrender.com/api/v1';

// Validation schema for property prediction
const predictionValidationSchema = Yup.object().shape({
  locality_name: Yup.string().required('Locality is required'),
  bhk: Yup.number().min(1).max(5).required('BHK is required'),
  carpet_area_sqft: Yup.number().min(300).required('Carpet area is required'),
  floor_number: Yup.number().nullable(),
  total_floors: Yup.number().nullable(),
  building_age_years: Yup.number().min(0).nullable(),
});

const LOCALITIES = [
  "Kharghar", "Vashi", "Panvel", "Nerul",
  "Belapur", "Airoli", "Ulwe", "Dronagiri",
  "CBD Belapur", "Seawoods", "Koparkhairane",
  "Ghansoli", "Kamothe", "Taloje"
];

export default function PricePredictor() {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (values, { setSubmitting }) => {
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await axios.post(
        `${API_BASE_URL}/prediction/predict`,
        values
      );
      setPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error generating prediction');
    } finally {
      setLoading(false);
      setSubmitting(false);
    }
  };

  const formatIndianPrice = (price) => {
    if (!price) return "₹ 0";

    if (price >= 10000000) {
      return `₹ ${(price / 10000000).toFixed(2)} Cr`;
    } 
    else if (price >= 100000) {
      return `₹ ${(price / 100000).toFixed(2)} Lakh`;
    } 
    else {
      return `₹ ${price.toLocaleString("en-IN")}`;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 p-4">
      <div className="max-w-6xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-2">
            Navi Mumbai House Price Predictor
          </h1>
          <p className="text-blue-100 text-lg">
            AI-powered property valuation for Navi Mumbai
          </p>
        </header>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Prediction Form */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              Get Price Estimate
            </h2>

            <Formik
              initialValues={{
                locality_name: '',
                bhk: 2,
                carpet_area_sqft: 1000,
                floor_number: '',
                total_floors: '',
                building_age_years: '',
                lift: false,
                parking: false,
                gym: false,
                swimming_pool: false,
                gated_society: false,
                cctv: false,
              }}
              validationSchema={predictionValidationSchema}
              onSubmit={handleSubmit}
            >
              {({ isSubmitting, values }) => (
                <Form className="space-y-4">
                  {/* Locality Selection */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Locality *
                    </label>
                    <Field
                      as="select"
                      name="locality_name"
                      className="w-full border border-gray-300 rounded px-3 py-2"
                    >
                      <option value="">Select a locality</option>
                      {LOCALITIES.map(loc => (
                        <option key={loc} value={loc}>{loc}</option>
                      ))}
                    </Field>
                    <ErrorMessage name="locality_name" component="div" className="text-red-500 text-sm mt-1" />
                  </div>

                  {/* BHK */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      BHK Configuration *
                    </label>
                    <Field
                      type="number"
                      name="bhk"
                      min="1"
                      max="5"
                      className="w-full border border-gray-300 rounded px-3 py-2"
                    />
                    <ErrorMessage name="bhk" component="div" className="text-red-500 text-sm mt-1" />
                  </div>

                  {/* Carpet Area */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Carpet Area (sq. ft.) *
                    </label>
                    <Field
                      type="number"
                      name="carpet_area_sqft"
                      min="300"
                      className="w-full border border-gray-300 rounded px-3 py-2"
                    />
                    <ErrorMessage name="carpet_area_sqft" component="div" className="text-red-500 text-sm mt-1" />
                  </div>

                  {/* Floor Info */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Floor Number
                      </label>
                      <Field
                        type="number"
                        name="floor_number"
                        className="w-full border border-gray-300 rounded px-3 py-2"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Total Floors
                      </label>
                      <Field
                        type="number"
                        name="total_floors"
                        className="w-full border border-gray-300 rounded px-3 py-2"
                      />
                    </div>
                  </div>

                  {/* Building Age */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Building Age (years)
                    </label>
                    <Field
                      type="number"
                      name="building_age_years"
                      min="0"
                      className="w-full border border-gray-300 rounded px-3 py-2"
                    />
                  </div>

                  {/* Amenities */}
                  <fieldset className="border-t pt-4 mt-4">
                    <legend className="text-sm font-medium text-gray-700 mb-3">
                      Amenities
                    </legend>
                    <div className="space-y-2">
                      {['lift', 'parking', 'gym', 'swimming_pool', 'gated_society', 'cctv'].map(amenity => (
                        <label key={amenity} className="flex items-center">
                          <Field
                            type="checkbox"
                            name={amenity}
                            className="h-4 w-4 text-blue-600"
                          />
                          <span className="ml-2 text-gray-700 capitalize">
                            {amenity.replace('_', ' ')}
                          </span>
                        </label>
                      ))}
                    </div>
                  </fieldset>

                  {/* Submit Button */}
                  <button
                    type="submit"
                    disabled={isSubmitting || loading}
                    className="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition duration-200"
                  >
                    {loading ? 'Predicting...' : 'Get Price Prediction'}
                  </button>

                  {error && (
                    <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                      {error}
                    </div>
                  )}
                </Form>
              )}
            </Formik>
          </div>

          {/* Prediction Results */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              Price Estimate
            </h2>

            {prediction ? (
              <div className="space-y-4">
                <div className="bg-gradient-to-br from-green-50 to-blue-50 border-2 border-green-200 rounded-lg p-6">
                  <p className="text-gray-600 text-sm">Estimated Total Price</p>
                  <p className="text-4xl font-bold text-green-600 mb-2">
                    {formatIndianPrice(prediction.predicted_total_price)}
                  </p>
                  <p className="text-gray-600 text-sm">
                    ₹{(prediction.predicted_price_per_sqft).toFixed(0)}/sq.ft.
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                    <p className="text-gray-600 text-sm">Lower Bound (80% CI)</p>
                    <p className="text-lg font-semibold text-blue-600">
                      {formatIndianPrice(prediction.lower_bound)}
                    </p>
                  </div>
                  <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                    <p className="text-gray-600 text-sm">Upper Bound (80% CI)</p>
                    <p className="text-lg font-semibold text-blue-600">
                      {formatIndianPrice(prediction.upper_bound)}
                    </p>
                  </div>
                </div>

                <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
                  <p className="text-gray-600 text-sm">Confidence Score</p>
                  <div className="mt-2">
                    <div className="w-full bg-purple-200 rounded-full h-2">
                      <div
                        className="bg-purple-600 h-2 rounded-full"
                        style={{ width: `${prediction.confidence_score * 100}%` }}
                      ></div>
                    </div>
                    <p className="text-sm text-purple-600 mt-1">
                      {(prediction.confidence_score * 100).toFixed(0)}%
                    </p>
                  </div>
                </div>

                <div className="text-gray-500 text-xs">
                  Prediction ID: {prediction.id}
                  <br />
                  Model: {prediction.model_version}
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-center h-64 text-center">
                <p className="text-gray-500">
                  Fill in the form and click "Get Price Prediction" to see results
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
